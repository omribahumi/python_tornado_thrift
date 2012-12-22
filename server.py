#!/usr/bin/python

import sys
sys.path.append('./gen-py')

from newservice import NewService
from newservice.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.server import TServer
from thrift.protocol import TBinaryProtocol
from TJSONProtocol import *
from thrift.server.THttpServer import THttpServer

from newservicehandler import NewServiceHandler

def main():
    handler = NewServiceHandler()
    processor = NewService.Processor(handler)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TJSONProtocolFactory()

    server = THttpServer(processor, ('0.0.0.0', 8888), pfactory)
    server.serve()

if __name__ == '__main__':
    main()
