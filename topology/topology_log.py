#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import os

# File to store the test results
test_phase1 = os.path.expanduser('~') + '/ik2220-assign-phase1-team5/results/phase_1_report.txt'

def topology():
    """Create a network."""
    net = Mininet(controller=RemoteController, link=TCLink, switch=OVSKernelSwitch)

    # Add controller
    c1 = net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Add switches
    info("*** Creating Switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    lb6 = net.addSwitch('lb6')
    lb7 = net.addSwitch('lb7')
    id8 = net.addSwitch('id8')
    n9 = net.addSwitch('n9')
    fw10 = net.addSwitch('fw10')
    fw11 = net.addSwitch('fw11')

    # Add hosts
    info("*** Creating Hosts\n")
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
    info("*** Creating Links\n")
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
    info("*** Starting Network\n")
    net.build()
    c1.start()
    for switch in [s1, s2, s3, s4, s5, lb6, lb7, id8, n9, fw