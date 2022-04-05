def handler_reasoner(network, store, msg):
	network.send_msg('bob', msg)
def handler_bob(network, store, msg):
	pass


sites = [
	("reasoner", dict(), handler_reasoner),
	("bob", dict(), handler_bob),
]
