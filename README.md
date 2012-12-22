python_tornado_thrift
=====================

Python Tornado serving Thrift HTTP requests.

Project layout:
1. server.py - regular Thrift HTTP server
2. server_tornado.py - Tornado powered Thrift HTTP server - accepts both POST and web socket transport protocols
3. client_post.py - regular Thrift client that uses POST (will work with both servers)
4. client_websocket.py - Thrift client that uses web sockets for transport
5. static/index.html - HTML client with Java script Thrift library - accessible through http://localhost:8888/static/index.html when running server_tornado.py

