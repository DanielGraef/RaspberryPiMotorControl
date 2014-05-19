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
	
	def __init__(self, pin):
		self.P1 = pin [0]
		self.P2 = pin [1]
		self.P3 = pin [2]
		self.P4 = pin [3]
		for p in pin:
			GPIO.setup(p, GPIO.OUT)
			GPIO.output(p, 0)

	StepDelay = 0.005

	def turn_motor_left(self):
                GPIO.output(self.P1, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P1, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P2, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P2, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P3, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P3, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P4, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)
	
	def turn_bipol_left(self):
		#1st step
		GPIO.output(self.P1, GPIO.HIGH)
		GPIO.output(self.P2, GPIO.LOW)
		GPIO.output(self.P3, GPIO.LOW)
		GPIO.output(self.P4, GPIO.HIGH)
		time.sleep(self.StepDelay)
		
		#2nd step
		GPIO.output(self.P1, GPIO.LOW)
                GPIO.output(self.P2, GPIO.HIGH)
                GPIO.output(self.P3, GPIO.LOW)
                GPIO.output(self.P4, GPIO.HIGH)
                time.sleep(self.StepDelay)
		
		#3rd step
		GPIO.output(self.P1, GPIO.LOW)
                GPIO.output(self.P2, GPIO.HIGH)
                GPIO.output(self.P3, GPIO.HIGH)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)
	
		#4rd Step
		GPIO.output(self.P1, GPIO.HIGH)
                GPIO.output(self.P2, GPIO.LOW)
                GPIO.output(self.P3, GPIO.HIGH)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)

	def turn_motor_right(self):
		GPIO.output(self.P4, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P3, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P3, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P2, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P2, GPIO.LOW)
                time.sleep(self.StepDelay)
                GPIO.output(self.P1, GPIO.HIGH)
                time.sleep(self.StepDelay)
                GPIO.output(self.P1, GPIO.LOW)
                time.sleep(self.StepDelay)

	def turn_bipol_right(self):
                #1st step
		GPIO.output(self.P1, GPIO.HIGH)
		GPIO.output(self.P2, GPIO.LOW)
                GPIO.output(self.P3, GPIO.HIGH)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)

                #2nd step
                GPIO.output(self.P1, GPIO.LOW) 
                GPIO.output(self.P2, GPIO.HIGH)
                GPIO.output(self.P3, GPIO.HIGH)
                GPIO.output(self.P4, GPIO.LOW)
                time.sleep(self.StepDelay)

                #3rd step
                GPIO.output(self.P1, GPIO.LOW) 
                GPIO.output(self.P2, GPIO.HIGH)
                GPIO.output(self.P3, GPIO.LOW)
                GPIO.output(self.P4, GPIO.HIGH)
                time.sleep(self.StepDelay)

                #4rd Step
                GPIO.output(self.P1, GPIO.HIGH)
                GPIO.output(self.P2, GPIO.LOW)
                GPIO.output(self.P3, GPIO.LOW)
                GPIO.output(self.P4, GPIO.HIGH)
                time.sleep(self.StepDelay)

			
m1 = Motor([3,5,7,8])
m2 = Motor([10,11,12,13])

StepCount = 0

def fader_callback(path, tags, args, source):
	print ("path", path)
	print("tags", tags) 
	print ("args", args[0]) 
	print ("source", source) 
	#msg=OSCMessage("/1/fader1")
	#msg.append(args);
	#client.send(msg)
 
	FaderValue = round(args[0]*100)
	print ("fadervalue", FaderValue) 	
	global StepCount

	if FaderValue > StepCount:
		while FaderValue > StepCount:
			StepCount += 1
			m1.turn_bipol_left()
			print ("stepcount", StepCount)
	
	elif FaderValue < StepCount:
		while FaderValue < StepCount:
			StepCount -= 1
			m1.turn_bipol_right()
			print("stepcount", StepCount)

server.addMsgHandler( "/1/fader1",fader_callback)

StepCount_m2 = 0

def fader_2_callback(path, tags, args, source):
        #print ("path", path) 
        #print ("args", args[0]) 
        #print ("source", source) 
        #msg=OSCMessage("/1/fader1")
        #msg.append(args);
        #client.send(msg)

        FaderValue = round(args[0])
        print ("fadervalue", FaderValue)
        global StepCount_m2

        if FaderValue > StepCount_m2:
                while FaderValue > StepCount_m2:
                        StepCount_m2 += 1
                        m2.turn_bipol_left()
                        print ("stepcount", StepCount_m2)

        elif FaderValue < StepCount_m2:
                while FaderValue < StepCount_m2:
                        StepCount_m2 -= 1
                        m2.turn_bipol_right()
                        print("stepcount", StepCount_m2)

server.addMsgHandler( "/1/fader2",fader_2_callback)

# Motorcontrol

def turn_motor_Left_handler(path, tags, args, source):
	motor_x_left = args
	print("args", motor_x_left)
	if motor_x_left == [1.0]:
		m1.turn_motor_left()
	else: 
		GPIO.output(3, GPIO.LOW)
		GPIO.output(5, GPIO.LOW)
		GPIO.output(7, GPIO.LOW)
		GPIO.output(8, GPIO.LOW)

server.addMsgHandler( "/1/pushLeft",turn_motor_Left_handler)

StepDelay = 0.1

def turn_motor_Right_handler(path, tags, args, source):
        motor_x_right = args
        print("args", motor_x_right)
        if motor_x_right == [1.0]:
		m1.turn_motor_right()	
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
		m2.turn_motor_left()
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
		m2.turn_motor_right()               
        else:
                GPIO.output(13, GPIO.LOW)
                GPIO.output(12, GPIO.LOW)
                GPIO.output(11, GPIO.LOW)
                GPIO.output(10, GPIO.LOW)

server.addMsgHandler( "/1/pushDown",turn_motor_Down_handler)

while True:
	server.handle_request()

server.close()
