#!/usr/bin/env python
from twisted.internet import defer, reactor

from txrospy import protocol_zeromq_thrift
from beginner_tutorials.genpythrift_twisted.AddTwoInts import AddTwoInts

import sys

from txzmq import ZmqFactory, ZmqEndpoint, ZmqREQConnection
import time
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TTwisted
from rosmaster.genpythrift_twisted.MasterAPI import MasterAPI


@defer.inlineCallbacks
def start_client():
    client = protocol_zeromq_thrift.ZeroMQThriftROSClient('add_two_ints',
        'unnamed', AddTwoInts.Client)
    proxy = yield client.wait_for_endpoint()

    p2 = yield proxy.add(1, 2)
    print p2

    p3 = yield proxy.add(1234567, 1)
    print p3

    reactor.stop()

if __name__ == '__main__':
    start_client()
    reactor.run()
