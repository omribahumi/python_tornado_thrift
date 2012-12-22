from thrift.transport.TTransport import TTransportBase
import websocket
from StringIO import StringIO

class TWebsocketClient(TTransportBase):
    """Tornado transport implementation using a websocket"""
    def __init__(self, url):
        self._url = url
        self._isopen = False
        self._wbuf = StringIO()
        self._rbuf = StringIO()
    
    def open(self):
        self._ws = websocket.WebSocket()
        self._ws.connect(self._url)
        self._isopen = True

    def close(self):
        self._isopen = False
        self._ws.close()

    def isOpen(self):
        return self._isopen

    def write(self, buf):
        self._wbuf.write(buf)

    def flush(self):
        self._ws.send(self._wbuf.getvalue())
        self._wbuf = StringIO()

    def read(self, sz):
        ret = self._rbuf.read(sz)
        if len(ret) < sz:
            self._rbuf = StringIO(self._ws.recv())
            ret += self.read(sz - len(ret))
        return ret

__all__ = ['TWebsocketClient']

