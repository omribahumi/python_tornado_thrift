#!/usr/bin/python

import sys
sys.path.append('./gen-py')

import os

from newservice import NewService
from newservice.ttypes import *

from thrift.server import TServer
from TJSONProtocol import *

from newservicehandler import NewServiceHandler

import tornado
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler


class DualHandler(WebSocketHandler):
    """This class lets you implement WebSocket and RequestHandler
    (except for the get() method) in the same class.
    I couldn't find any reason why not to use the same handler both for
    websockets and POST calls, however, tornado doesn't let you do it.
    This is my workaround.
    """

    def _execute(self, *args, **kwargs):
        """Does the exact same thing like WebSocketHandler._execute() for GET
        requests. Otherwise, acts like RequestHandler.
        """
        if self.request.method == 'GET':
            # dispatch to WebSocketHandler
            WebSocketHandler._execute(self, *args, **kwargs)
        else:
            # remap unsupported WebSocketHandler methods back to RequestHandler
            # the __get__(self, DualHandler) trick is used to bind the methods
            # back to the object, otherwise it's unbound
            for method in ["write", "redirect", "set_header", "send_error",
                           "set_cookie", "set_status", "flush", "finish"]:
                    setattr(self, method,
                            getattr(RequestHandler, method).__get__(
                                    self, DualHandler))
 
            # dispatch to RequestHandler
            RequestHandler._execute(self, *args, **kwargs)
 

class ThriftDualHandler(DualHandler, TServer.TServer):
    def initialize(self, processor, inputProtocolFactory,
                  outputProtocolFactory):
        TServer.TServer.__init__(self, processor, None, None, None,
            inputProtocolFactory, outputProtocolFactory)

    def post(self):
        self.set_header('Content-Type', 'application/x-thrift')
        self.write(self.handle_request(self.request.body))

    def on_message(self, message):
        self.write_message(self.handle_request(message))

    def handle_request(self, data):
        itrans = TTransport.TMemoryBuffer(data)
        otrans = TTransport.TMemoryBuffer()
        iprot = self.inputProtocolFactory.getProtocol(itrans)
        oprot = self.outputProtocolFactory.getProtocol(otrans)
        self.processor.process(iprot, oprot)
        return otrans.getvalue()

def main():
    handler = NewServiceHandler()
    processor = NewService.Processor(handler)
    pfactory = TJSONProtocolFactory()

    application = tornado.web.Application([
        (r"/thrift", ThriftDualHandler,
            dict(processor=processor, inputProtocolFactory=pfactory,
                 outputProtocolFactory=pfactory)),
        (r"/static/(.*)", tornado.web.StaticFileHandler,
            {"path": os.path.join(os.path.dirname(__file__), "static"),
             "default_filename" : "index.html"}),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

