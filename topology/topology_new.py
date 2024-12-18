#!/usr/bin/python

"""
Script created by VND - Visual Network Description (SDN version)
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSLegacyKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology():
    print("Create a network.")
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633, mac='00:00:00:00:00:0d' )
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:02' )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:03' )
    s3 = net.addSwitch( 's3', listenPort=6634, mac='00:00:00:00:00:04' )
    s4 = net.addSwitch( 's4', listenPort=6634, mac='00:00:00:00:00:05' )
    s5 = net.addSwitch( 's5', listenPort=6634, mac='00:00:00:00:00:06' )
    lb6 = net.addSwitch( 'lb6', listenPort=6634, mac='00:00:00:00:00:07' )
    lb7 = net.addSwitch( 'lb7', listenPort=6634, mac='00:00:00:00:00:08' )
    id8 = net.addSwitch( 'id8', listenPort=6634, mac='00:00:00:00:00:09' )
    n9 = net.addSwitch( 'n9',listenPort=6634, mac='00:00:00:00:00:0a' )
    fw10 = net.addSwitch ('fw10', listenPort = 6634, mac='00:00:00:00:00:0b')
    fw11 = net.addSwitch ('fw11' ,listenPort = 6634, mac='00:00:00:00:00:0c')
    h1 = net.addHost( 'h1', ip='100.0.0.11/24' )
    h2 = net.addHost( 'h2', ip='100.0.0.12/24' )
    h3 = net.addHost( 'h3', ip='100.0.0.51/24' )
    h4 = net.addHost( 'h4', ip='100.0.0.52/24' )
    ws5 = net.addHost( 'ws5', ip='100.0.0.40/24' )
    ws6 = net.addHost( 'ws6', ip='100.0.0.41/24' )
    ws7 = net.addHost( 'ws7', ip='100.0.0.42/24' )
    ds8 = net.addHost( 'ds8', ip='100.0.0.20/24' )
    ds9 = net.addHost( 'ds9', ip='100.0.0.21/24' )
    ds10 = net.addHost( 'ds10', ip = '100.0.0.22/24')
    insp11 = net.addHost( 'insp11',ip = '100.0.0.30/24')

    print ("*** Creating links")
    net.addLink(s1,h1)
    net.addLink(s1,h2)
    net.addLink(s1,fw10)
    net.addLink(s2,fw10)
    
    net.addLink(s2,fw11)
    net.addLink(s2,id8)
    net.addLink(s2,lb6)
    net.addLink(s3,ds8)
    net.addLink(s3,ds9)
    net.addLink(s3,ds10)
    net.addLink(s3,lb6)
    net.addLink(s4,ws5)
    net.addLink(s4,ws6)
    net.addLink(s4,ws7)
    net.addLink(s4,lb7)
    net.addLink(lb7,id8)
    net.addLink(n9,fw11)
    net.addLink(s5, h3)
    net.addLink(s5, h4)
    net.addLink(s5,n9)
    net.addLink(id8,insp11)

    print("*** Starting network")
    net.build()
    s1.start( [c1] )
    s2.start( [c1] )
    s3.start( [c1] )
    s4.start( [c1] )
    s5.start( [c1] )
    lb6.start( [c1] )
    lb7.start( [c1] )
    id8.start( [c1] )
    n9.start( [c1] )
    fw10.start( [c1] )
    fw11.start( [c1] )
    print ("Done")

    print("*** Running CLI")
    CLI( net )

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
