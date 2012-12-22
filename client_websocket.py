#!/usr/bin/python
 
import sys
sys.path.append('./gen-py')
 
from newservice import NewService
from newservice.ttypes import *
 
from thrift.transport import THttpClient
from TJSONProtocol import *
from TWebsocketClient import *

def main():
    transport = TWebsocketClient("ws://localhost:8888/thrift")
    protocol = TJSONProtocol(transport)
    client = NewService.Client(protocol)
    transport.open()
    print client.strcat('client', 'websocket')
    transport.close()

if __name__ == '__main__':
    main()

