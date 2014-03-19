from OSC import OSCServer,OSCClient, OSCMessage
import sys
import time
import types
import RPi.GPIO as GPIO

#GPIO Setup

GPIO.setmode(GPIO.BOARD)


#OSC Server Setup

server = OSCServer( ("0.0.0.0", 8000) )
client = OSCClient()
client.connect( ("192.168.178.2", 9000) )

def handle_timeout(self):
	print ("Timeout")

server.handle_timeout = types.MethodType(handle_timeout, server)

class Motor(object):
        def __init__(self):
                GPIO.setup(3, GPIO.OUT)
                GPIO.setup(5, GPIO.OUT)
                GPIO.setup(7, GPIO.OUT)
                GPIO.setup(8, GPIO.OUT)
                GPIO.setup(10, GPIO.OUT)
                GPIO.setup(11, GPIO.OUT)
                GPIO.setup(12, GPIO.OUT)
                GPIO.setup(13, GPIO.OUT)

        def turn_motor_x_left(self):
                GPIO.output(3, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(3, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(5, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(5, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(7, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(7, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(8, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(8, GPIO.LOW)
                time.sleep(StepDelay)

        def turn_motor_x_right(self):
                GPIO.output(8, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(8, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(7, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(7, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(5, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(5, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(3, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(3, GPIO.LOW)
                time.sleep(StepDelay)

        def turn_motor_y_Up(self):
                GPIO.output(10, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(10, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(11, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(11, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(12, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(12, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(13, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(13, GPIO.LOW)
                time.sleep(StepDelay)

        def turn_motor_y_Down(self):
               GPIO.output(13, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(13, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(12, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(12, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(11, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(11, GPIO.LOW)
                time.sleep(StepDelay)
                GPIO.output(10, GPIO.HIGH)
                time.sleep(StepDelay)
                GPIO.output(10, GPIO.LOW)
                time.sleep(StepDelay)

m = Motor()

def fader_callback(path, tags, args, source):
	print ("path", path) 
	print ("args", args) 
	print ("source", source) 
	msg=OSCMessage("/1/rotary1")
	msg.append(args);
	client.send(msg)


server.addMsgHandler( "/1/fader1",fader_callback)

#GPIO Reset

GPIO.output(3, GPIO.LOW)
GPIO.output(5, GPIO.LOW)
GPIO.output(7, GPIO.LOW)
GPIO.output(8, GPIO.LOW)
GPIO.output(10, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

# Motorcontrol

StepDelay = 0.1

def turn_motor_Left_handler(path, tags, args, source):
	motor_x_left = args
	print("args", motor_x_left)
	if motor_x_left == [1.0]:
		m.turn_motor_Left()
	else: 
		GPIO.output(3, GPIO.LOW)
		GPIO.output(5, GPIO.LOW)
		GPIO.output(7, GPIO.LOW)
		GPIO.output(8, GPIO.LOW)

server.addMsgHandler( "/1/pushLeft",turn_motor_Left_handler)

def turn_motor_Right_handler(path, tags, args, source):
        motor_x_right = args
        print("args", motor_x_right)
        if motor_x_right == [1.0]:
                m.turn_motor_right
        else:
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
                GPIO.output(5, GPIO.LOW)
                GPIO.output(3, GPIO.LOW)

server.addMsgHandler( "/1/pushRight",turn_motor_Right_handler)

def turn_motor_Up_handler(path, tags, args, source):
        motor_y_up = args
        print("args", motor_y_up)
        if motor_y_up == [1.0]:
                m.turn_motor_y_Up()
        else:
                GPIO.output(10, GPIO.LOW)
                GPIO.output(11, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)

server.addMsgHandler( "/1/pushUp",turn_motor_Up_handler)

def turn_motor_Down_handler(path, tags, args, source):
        motor_y_down = args
        print("args", motor_y_down)
        if motor_y_down == [1.0]:
                m.turn_motor_y_Down
        else:
                GPIO.output(13, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)
                GPIO.output(11, GPIO.LOW)
                GPIO.output(10, GPIO.LOW)

server.addMsgHandler( "/1/pushDown",turn_motor_Down_handler)

while True:
	server.handle_request()

server.close()
