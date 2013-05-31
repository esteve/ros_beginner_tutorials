#!/usr/bin/env python
from twisted.application import service, internet
from twisted.internet import defer, reactor

from txrospy import protocol_zeromq_thrift
from beginner_tutorials.genpythrift_twisted.AddTwoInts import AddTwoInts
import zope

class AddTwoIntsHandler(object):
  zope.interface.implements(AddTwoInts.Iface)

  def add(self, a, b):
    print "Adding a (%d) and b (%d)" % (a, b)
    response = a + b
    d = defer.Deferred()
    # Simulate a long-running computation
    reactor.callLater(0.1, d.callback, response)
    return d


@defer.inlineCallbacks
def main():
    server = 'add_two_ints_server'
    ros_service_name = 'add_two_ints'
    ros_rpc_port = 12345
    zeromq_rpc_port = 58260
    hostname = '127.0.0.1'
    caller_api = 'zeromq+thrift://%s:%d/' % (hostname, zeromq_rpc_port)
    rpc_uri = 'zeromq+thrift://%s:%d' % (hostname, ros_rpc_port)

    handler = AddTwoInts.Processor(AddTwoIntsHandler())

    service = protocol_zeromq_thrift.ZeroMQThriftROSService(handler, AddTwoInts,
        server, ros_service_name, rpc_uri, caller_api)
    yield service.initialize()

if __name__ == '__main__':
    main()
    reactor.run()
