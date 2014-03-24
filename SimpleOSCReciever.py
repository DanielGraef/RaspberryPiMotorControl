from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import types

server = OSCServer( ("0.0.0.0", 8000) )
client = OSCClient()
client.connect( ("192.168.1.2", 9000) )

def handle_timeout(self):
	print ("Timeout")

server.handle_timeout = types.MethodType(handle_timeout, server)

def fader_callback(path, tags, args, source):
	print ("path", path) 
	print ("args", args) 
	print ("source", source) 
	msg=OSCMessage("/1/rotary1")
	msg.append(args);
	client.send(msg)


server.addMsgHandler( "/1/fader1",fader_callback)

while True:
	server.handle_request()

server.close()


