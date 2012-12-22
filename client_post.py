#!/usr/bin/python
 
import sys
sys.path.append('./gen-py')
 
from newservice import NewService
from newservice.ttypes import *
 
from thrift.transport import THttpClient
from TJSONProtocol import *
 
def main():
    transport = THttpClient.THttpClient("http://localhost:8888/thrift")
    protocol = TJSONProtocol(transport)
    client = NewService.Client(protocol)
    transport.open()
    print client.strcat('client', 'post')
    transport.close()

if __name__ == '__main__':
    main()

