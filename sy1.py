"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1Host = self.addHost( 'h1' )
	h2Host = self.addHost( 'h2' )
	h3Host = self.addHost( 'h3' )
	h4Host = self.addHost( 'h4' )
	h5Host = self.addHost( 'h5' )
	h6Host = self.addHost( 'h6' )
	h7Host = self.addHost( 'h7' )
	h8Host = self.addHost( 'h8' )

	s1Switch = self.addSwitch( 's1' )
	s2Switch = self.addSwitch( 's2' )
	s3Switch = self.addSwitch( 's3' )
	s4Switch = self.addSwitch( 's4' )
	s5Switch = self.addSwitch( 's5' )
	s6Switch = self.addSwitch( 's6' )
	s7Switch = self.addSwitch( 's7' )

        # Add links
        self.addLink( h1Host, s4Switch )
	self.addLink( h2Host, s4Switch )
	self.addLink( h3Host, s5Switch )
	self.addLink( h4Host, s5Switch )
	self.addLink( h5Host, s6Switch )
	self.addLink( h6Host, s6Switch )
	self.addLink( h7Host, s7Switch )
	self.addLink( h8Host, s7Switch )

        self.addLink( s4Switch, s2Switch )
	self.addLink( s5Switch, s2Switch )
	self.addLink( s6Switch, s3Switch )
	self.addLink( s7Switch, s3Switch )
	self.addLink( s2Switch, s1Switch )
	self.addLink( s3Switch, s1Switch )

topos = { 'mytopo': ( lambda: MyTopo() ) }
