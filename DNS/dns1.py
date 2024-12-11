import socket
import glob
import json

# DNS Server Configuration
port = 53
ip = '100.0.0.20'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

# Load DNS zones from files
def load_zones():
    jsonzone = {}
    zonefiles = glob.glob('zones/*.zone')

    for zone in zonefiles:
        with open(zone) as zonedata:
            data = json.load(zonedata)
            zonename = data["$origin"]
            jsonzone[zonename] = data
    return jsonzone

zonedata = load_zones()

# Parse DNS flags from the request
def getflags(flags):
    byte1 = flags[0]
    byte2 = flags[1]

    QR = '1'  # This is a response
    OPCODE = ''.join([str((byte1 >> bit) & 1) for bit in range(1, 5)])
    AA = '1'  # Authoritative Answer
    TC = '0'  # Truncation
    RD = '0'  # Recursion Desired

    RA = '0'  # Recursion Available
    Z = '000' # Reserved
    RCODE = '0000' # Response Code

    return int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder='big') + int(RA + Z + RCODE, 2).to_bytes(1, byteorder='big')

# Extract the question domain from the DNS query
def getquestiondomain(data):
    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    offset = 0

    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            offset += 1
            if offset == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
                offset = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte

    questiontype = data[offset + 1:offset + 3]
    return domainparts, questiontype

# Get zone information for a domain
def getzone(domain):
    global zonedata
    zone_name = '.'.join(domain)
    if zone_name in zonedata:
        return zonedata[zone_name]
    return None

# Retrieve records for a DNS query
def getrecs(data):
    domain, questiontype = getquestiondomain(data)
    qt = ''
    if questiontype == b'\x00\x01':
        qt = 'a'

    zone = getzone(domain)
    if zone and qt in zone:
        return zone[qt], qt, domain

    return [], qt, domain

# Build the DNS question section
def buildquestion(domainname, rectype):
    qbytes = b''

    for part in domainname:
        length = len(part)
        qbytes += bytes([length])
        qbytes += part.encode('utf-8')

    if rectype == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')

    qbytes += (1).to_bytes(2, byteorder='big')
    return qbytes

# Convert a record to bytes for the DNS response
def rectobytes(domainname, rectype, recttl, recval):
    rbytes = b'\xc0\x0c'

    if rectype == 'a':
        rbytes += (0).to_bytes(1, byteorder='big') + (1).to_bytes(1, byteorder='big')

    rbytes += (0).to_bytes(1, byteorder='big') + (1).to_bytes(1, byteorder='big')
    rbytes += int(recttl).to_bytes(4, byteorder='big')

    if rectype == 'a':
        rbytes += (4).to_bytes(2, byteorder='big')
        rbytes += bytes(map(int, recval.split('.')))

    return rbytes

# Build the DNS response
def buildresponse(data):
    # Transaction ID
    TransactionID = data[:2]

    # Get the flags
    Flags = getflags(data[2:4])

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Get answer records
    records, rectype, domainname = getrecs(data[12:])

    # Answer Count
    ANCOUNT = len(records).to_bytes(2, byteorder='big')

    # Nameserver and Additional Counts
    NSCOUNT = (0).to_bytes(2, byteorder='big')
    ARCOUNT = (0).to_bytes(2, byteorder='big')

    dnsheader = TransactionID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

    # Create DNS body
    dnsbody = b''
    dnsquestion = buildquestion(domainname, rectype)

    for record in records:
        dnsbody += rectobytes(domainname, rectype, record["ttl"], record["value"])

    return dnsheader + dnsquestion + dnsbody

# Main DNS server loop
while True:
    data, addr = sock.recvfrom(512)
    try:
        response = buildresponse(data)
        sock.sendto(response, addr)
    except Exception as e:
        print(f"Error handling request: {e}")
