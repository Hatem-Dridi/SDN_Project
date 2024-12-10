#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import os

test_phase1 = os.path.expanduser('~/results/Report_phase1')  # Fixed the path

def topology():
    "Create a network."
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    # Begin controller
    c1 = net.addController('c1', controller=RemoteController, ip='172.17.0.2', port=6633, mac='02:42:ac:11:00:02')

    # Add switches
    print("*** Creating Switches")
    s1 = net.addSwitch('s1', listenPort=6634, mac='00:00:00:00:00:02')
    s2 = net.addSwitch('s2', listenPort=6634, mac='00:00:00:00:00:03')
    s3 = net.addSwitch('s3', listenPort=6634, mac='00:00:00:00:00:04')
    s4 = net.addSwitch('s4', listenPort=6634, mac='00:00:00:00:00:05')
    s5 = net.addSwitch('s5', listenPort=6634, mac='00:00:00:00:00:06')
    lb6 = net.addSwitch('lb6', listenPort=6634, mac='00:00:00:00:00:07')
    lb7 = net.addSwitch('lb7', listenPort=6634, mac='00:00:00:00:00:08')
    id8 = net.addSwitch('id8', listenPort=6634, mac='00:00:00:00:00:09')
    n9 = net.addSwitch('n9', listenPort=6634, mac='00:00:00:00:00:0a')
    fw10 = net.addSwitch('fw10', listenPort=6634, mac='00:00:00:00:00:0b')
    fw11 = net.addSwitch('fw11', listenPort=6634, mac='00:00:00:00:00:0c')

    # Add hosts
    print("*** Creating Hosts")
    h1 = net.addHost('h1', ip='100.0.0.11/24')
    h2 = net.addHost('h2', ip='100.0.0.12/24')
    h3 = net.addHost('h3', ip='100.0.0.51/24')
    h4 = net.addHost('h4', ip='100.0.0.52/24')
    ws5 = net.addHost('ws5', ip='100.0.0.40/24')
    ws6 = net.addHost('ws6', ip='100.0.0.41/24')
    ws7 = net.addHost('ws7', ip='100.0.0.42/24')
    ds8 = net.addHost('ds8', ip='100.0.0.20/24')
    ds9 = net.addHost('ds9', ip='100.0.0.21/24')
    ds10 = net.addHost('ds10', ip='100.0.0.22/24')
    insp11 = net.addHost('insp11', ip='100.0.0.30/24')

    # Add links
    print("*** Creating Links")
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, fw10)
    net.addLink(s2, fw10)
    net.addLink(s2, fw11)
    net.addLink(s2, id8)
    net.addLink(s2, lb6)
    net.addLink(s3, ds8)
    net.addLink(s3, ds9)
    net.addLink(s3, ds10)
    net.addLink(s3, lb6)
    net.addLink(s4, ws5)
    net.addLink(s4, ws6)
    net.addLink(s4, ws7)
    net.addLink(s4, lb7)
    net.addLink(lb7, id8)
    net.addLink(n9, fw11)
    net.addLink(s5, h3)
    net.addLink(s5, h4)
    net.addLink(s5, n9)
    net.addLink(id8, insp11)

    # Start the network
    print("*** Starting Network")
    net.build()
    s1.start([c1])
    s2.start([c1])
    s3.start([c1])
    s4.start([c1])
    s5.start([c1])
    lb6.start([c1])
    lb7.start([c1])
    id8.start([c1])
    n9.start([c1])
    fw10.start([c1])
    fw11.start([c1])
    print("Done")
    test_start(net)

def test_start(net):
    log = open(test_phase1, 'w+')
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    ds8 = net.get('ds8')
    ws5 = net.get('ws5')
    insp11 = net.get('insp11')

    # Capture traffic on insp11
    insp11.cmd("tcpdump -s 0 -i insp11-eth0 -w insp11.pcap &")

    # Ping tests
    output = h1.cmdPrint('ping -c5', h2.IP())
    log.write('Within Public Zone, ---h1 ping h2---\n'+output+'\n')

    output = h1.cmdPrint('ping -c5', h3.IP())
    log.write('Public to Private Zone ---h1 ping h3---\n'+output+'\n')

    output = h1.cmdPrint('ping -c5', h4.IP())
    log.write('Public to Private ---h1 ping h4---\n'+output+'\n')

    output = h3.cmdPrint('ping -c5', h4.IP())
    log.write('Within Private Zone ---h3 ping h4---\n'+output+'\n')

    output = h3.cmdPrint('ping -c5', h1.IP())
    log.write('Private to Public ---h3 ping h1---\n'+output+'\n')

    output = h3.cmdPrint('ping -c5', h2.IP())
    log.write('Private to Public ---h3 ping h2---\n'+output+'\n')

    # Further tests (DNS queries, IDS tests, etc.) go here...

    log.close()
    CLI(net)

    # Stop the network
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')  # Set logging level
    topology()
