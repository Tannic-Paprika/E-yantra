'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
# from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def get_vision_data(sim):

	visionSensorHandle = sim.getObjectHandle('vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)  #Capturing image from sensor
	img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)		
	img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
	# cv2.imshow("image",edged)
	# cv2.circle(img,(260,5),2,(0,0,0),2)
	cv2.imshow("image_1",img) 
	cv2.waitKey(1)
	


	if 0xff == ord('q'):
		cv2.destroyAllWindows()
		

	return img 

def setSpeed (speed):
	left_joint = sim.getObjectHandle('left_joint')
	right_joint = sim.getObjectHandle('right_joint')

	sim.setJointTargetVelocity(left_joint, speed)
	sim.setJointTargetVelocity(right_joint, speed)

def pid(kp,kd):
	img = get_vision_data(sim)

	left_joint = sim.getObjectHandle('left_joint')
	right_joint = sim.getObjectHandle('right_joint')
	
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	
	pix = gray[400,262]

	ret,thresh1 = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)		
	# blurred = cv2.blur(thresh1, (1, 1))

	# Find Canny edges
	edged = cv2.Canny(thresh1, 85, 200)
	borderout=cv2.copyMakeBorder(edged,1,1,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
	
	contours, hierarchy = cv2.findContours(borderout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	

	if len(contours) > 0 :

		c = max(contours, key=cv2.contourArea)
		M = cv2.moments(c)

		if M["m00"] !=0 :
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

	kp = 0.0015
	error = cx - 260

	adjustment = kp*error  #kd*(error-last_error)

	sim.setJointTargetVelocity(left_joint , 0.2 + adjustment)
	sim.setJointTargetVelocity(right_joint , 0.2 - adjustment)

	

##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############

	left_joint = sim.getObjectHandle('left_joint')
	right_joint = sim.getObjectHandle('right_joint')
	global chk 



	def left():

		img = get_vision_data(sim)

		left_joint = sim.getObjectHandle('left_joint')
		right_joint = sim.getObjectHandle('right_joint')
		
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		
		pix = gray[400,262]

		ret,thresh1 = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)		
		# blurred = cv2.blur(thresh1, (1, 1))

		# Find Canny edges
		edged = cv2.Canny(thresh1, 85, 200)
		borderout=cv2.copyMakeBorder(edged,1,1,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
		
		contours, hierarchy = cv2.findContours(borderout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		

		if len(contours) > 0 :

			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)

			if M["m00"] !=0 :
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])

		
		
		
		while True : 
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			if (gray[cy ,cx] == 255 and gray[cy-100,cx+50] ==255):
				break
			
			
			sim.setJointTargetVelocity(left_joint,-0.2)
			sim.setJointTargetVelocity(right_joint,0.2)
			
		while gray[cy,cx] != 154 :  #Grey
			
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			sim.setJointTargetVelocity(left_joint,-0.2)
			sim.setJointTargetVelocity(right_joint,0.2)

		while gray[cy,cx] != 255 and gray[cy-70,cx] !=255: 
			
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			sim.setJointTargetVelocity(left_joint,-0.2)
			sim.setJointTargetVelocity(right_joint,0.2)	

		setSpeed(0)
		chk = "Turned"
		print(chk)
	
#######################################################################
	def right():

		img = get_vision_data(sim)

		left_joint = sim.getObjectHandle('left_joint')
		right_joint = sim.getObjectHandle('right_joint')
		
		gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
		
		pix = gray[400,262]

		ret,thresh1 = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)		
		# blurred = cv2.blur(thresh1, (1, 1))

		# Find Canny edges
		edged = cv2.Canny(thresh1, 85, 200)
		borderout=cv2.copyMakeBorder(edged,1,1,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
		
		contours, hierarchy = cv2.findContours(borderout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		

		if len(contours) > 0 :

			c = max(contours, key=cv2.contourArea)
			M = cv2.moments(c)

			if M["m00"] !=0 :
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])

		while True : 
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			if (gray[cy ,cx] == 255 and gray[cy-100,cx-50] ==255):
				break
		
			
			sim.setJointTargetVelocity(left_joint,0.2)
			sim.setJointTargetVelocity(right_joint,-0.2)

		while gray[cy,cx] != 154 :  #Grey
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			sim.setJointTargetVelocity(left_joint,0.2)
			sim.setJointTargetVelocity(right_joint,-0.2)

		while gray[cy-70,cx] != 255 and gray[cy,cx] != 255  : 
			img = get_vision_data(sim)
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			sim.setJointTargetVelocity(left_joint,0.2)
			sim.setJointTargetVelocity(right_joint,-0.2)	
				
		setSpeed(0)
		chk = "Turned"
		print(chk)
#######################################################################
	def follow_line():
		chk = "Follow Line"	
		while True:
			img = get_vision_data(sim)

			left_joint = sim.getObjectHandle('left_joint')
			right_joint = sim.getObjectHandle('right_joint')
			
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			
			pix = gray[400,262]

			ret,thresh1 = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)		
			

			# Find Canny edges
			edged = cv2.Canny(thresh1, 85, 200)
			borderout=cv2.copyMakeBorder(edged,1,1,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
			
			contours, hierarchy = cv2.findContours(borderout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			

			if len(contours) > 0 :

				c = max(contours, key=cv2.contourArea)
				M = cv2.moments(c)

				if M["m00"] !=0 :
					cx = int(M['m10']/M['m00'])
					cy = int(M['m01']/M['m00'])
			
			error = cx - 260 

			kp = 0.00416
			kd = 0
			last_error = 0
			if chk == "Follow Line":

				if pix > 153 or pix < 140:

					
					adjustment = kp*error + kd*(error-last_error)

					sim.setJointTargetVelocity(left_joint , 0.3 + adjustment)
					sim.setJointTargetVelocity(right_joint , 0.3 - adjustment)

					last_error = error 
					

				else:
					setSpeed(0)
					chk = "Reached Junction"
					print(chk)
					time.sleep(0.1)
				
			if chk == "Reached Junction":
				# print(gray[0,cx])
				while gray[0,cx+1] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] != 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				
				while gray[0,cx] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] != 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				setSpeed(0)
				time.sleep(0.1)
				print("Reached Centre")
				break

	def line_qr(checkpoint):
		chk = "Follow Line"	
		while True:
			img = get_vision_data(sim)

			left_joint = sim.getObjectHandle('left_joint')
			right_joint = sim.getObjectHandle('right_joint')
			
			gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
			
			pix = gray[400,262]

			ret,thresh1 = cv2.threshold(gray,85,255,cv2.THRESH_BINARY)		
			

			# Find Canny edges
			edged = cv2.Canny(thresh1, 85, 200)
			borderout=cv2.copyMakeBorder(edged,1,1,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
			
			contours, hierarchy = cv2.findContours(borderout, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			

			if len(contours) > 0 :

				c = max(contours, key=cv2.contourArea)
				M = cv2.moments(c)

				if M["m00"] !=0 :
					cx = int(M['m10']/M['m00'])
					cy = int(M['m01']/M['m00'])
			
			error = cx - 260 

			kp = 0.00416
			kd = 0
			last_error = 0
			if chk == "Follow Line":

				if pix > 153 or pix < 140:

					
					adjustment = kp*error + kd*(error-last_error)

					sim.setJointTargetVelocity(left_joint , 0.3 + adjustment)
					sim.setJointTargetVelocity(right_joint , 0.3 - adjustment)

					last_error = error 
					

				else:
					setSpeed(0)
					chk = "Reached Junction"
					print(chk)
					time.sleep(0.1)

			if chk == "Read Qr":
				arena_dummy_handle = sim.getObject("/Arena_dummy") 

				## Retrieve the handle of the child script attached to the Arena_dummy scene object.
				childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

				## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
				sim.callScriptFunction("activate_qr_code", childscript_handle, checkpoint)

				img = get_vision_data(sim)
				time.sleep(5)


			if chk == "Reached Junction":
				# print(gray[0,cx])
				while gray[0,cx+1] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] != 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				
				while gray[0,cx] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] != 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				while gray[0,cx] == 255 :
					img = get_vision_data(sim)
					gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
					pid(0.0015,0)
				setSpeed(0)
				time.sleep(0.1)
				print("Reached Centre")
				break			

		
	
	setSpeed(0)
	follow_line() 
	left() #A
	print("Reached A")
	follow_line()
	right()
	print("Reached B") #B
	follow_line()
	left()
	print("Reached C") #C
	follow_line() 
	right() #D
	print("Reached D")
	follow_line()#E
	arena_dummy_handle = sim.getObject("/Arena_dummy") 

	## Retrieve the handle of the child script attached to the Arena_dummy scene object.
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

	## Call the activate_qr_code() function defined in the child script to make the QR code visible at checkpoint E
	sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint E")
	message = read_qr_code(sim)
	print(message)
	img = get_vision_data(sim)
	time.sleep(5)
	
	print("Reached E")
	follow_line() #F
	print("Reached F")
	right()
	follow_line() #G
	print("Reached G")
	left()
	follow_line() #H
	print("Reached H")
	right()
	follow_line() #I
	print("Reached I")
	follow_line() #J 
	print("Reached J")
	right()
	follow_line() #K
	print("Reached K")
	left() 
	follow_line() #L
	print("Reached L")
	right()
	follow_line() #M
	print("Reached M")
	follow_line() #N
	print("Reached N")
	right()
	follow_line() #O
	print("Reached O")
	left()
	follow_line() #P
	print("Reached P")
	right()
	follow_line() #A
	print("Reached Endpoint")
	
	print('Program ended')

	##################################################


def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	##############  ADD YOUR CODE HERE  ##############
	img= get_vision_data(sim)
	# barcodes = decode(img)
	# bdata= barcodes[0].data.decode("utf-8")
	qr_message= f"{bdata}"
	
		
	
	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			control_logic(sim)
			# time.sleep(5)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()