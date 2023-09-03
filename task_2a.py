'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi, Sai Ram Senapati, Raj Pattnaik, Ashish Kumar Sahu ]
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2, detect_distance_sensor_3
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
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order
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

	def setSpeed (speed, error):
		# error= error +1
		# print(error)
  
		sim.setJointTargetVelocity(left_joint, speed + error)
		sim.setJointTargetVelocity(right_joint, speed - error)


	def rotateLeft(speed):
		ds1 = detect_distance_sensor_1(sim)
		
		while (ds1!=0 ):
			ds1 = detect_distance_sensor_1(sim)
			sim.setJointTargetVelocity(left_joint, -speed)
			sim.setJointTargetVelocity(right_joint,speed)
		setSpeed(0,0)
		while (True):
			prev_val=detect_distance_sensor_2(sim)
			sim.setJointTargetVelocity(left_joint,-speed/3)
			sim.setJointTargetVelocity(right_joint,speed/3)
			after_val=detect_distance_sensor_2(sim)
			# print("rotateLeft")
   
			if (after_val>prev_val):
				break
		
				
		setSpeed(0, 0)
		time.sleep(0.05)


	def rotateRight(speed):

		ds1 = detect_distance_sensor_1(sim)
		
		while (ds1!=0 ):
			ds1 = detect_distance_sensor_1(sim)
			sim.setJointTargetVelocity(left_joint, speed)
			sim.setJointTargetVelocity(right_joint, -speed)
		setSpeed(0,0)
		while (True):
			prev_val=detect_distance_sensor_3(sim)
			sim.setJointTargetVelocity(left_joint,speed/3)
			sim.setJointTargetVelocity(right_joint,-speed/3)
			after_val=detect_distance_sensor_3(sim)
			# print("rotateRight")
			if (after_val>prev_val):
				break
		
				
		setSpeed(0, 0)
		time.sleep(0.05)
	left_joint = sim.getObjectHandle('left_joint')  #Definingjoints
	right_joint = sim.getObjectHandle('right_joint')


	ds1 = detect_distance_sensor_1(sim)  #Checking the sensor value first
	
	setSpeed(0, 0)
	target_speed = 6
	x=0.5
	while True:

		ds1 = detect_distance_sensor_1(sim)
		# ds2 = detect_distance_sensor_2(sim)
		# ds3 = detect_distance_sensor_3(sim)
		
		if (0 < ds1 < 0.32):
			setSpeed(0, 0)
			time.sleep(0.05) 

			####Reached Centre
			
				
			ds2 = detect_distance_sensor_2(sim)
			ds3 = detect_distance_sensor_3(sim)
			if ds2 == 0 and ds3 !=0 :

				rotateRight(3)
				x=1
    
			elif ds2 !=0 and ds3 == 0 :
				rotateLeft(3)
				x=1
			elif ds2!=0 and ds1!=0 and ds3!=0 :
				break

			
		else:
			ds2 = detect_distance_sensor_2(sim)
			ds3 = detect_distance_sensor_3(sim)
			error = ds2 - 0.175
			if (x<=6.5):
				x+=0.9
			setSpeed(x, error)
				# print("straight")
				
					


	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	s1 = sim.getObjectHandle('distance_sensor_1')
	result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.readProximitySensor(s1)




	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	s2 = sim.getObjectHandle('distance_sensor_2')
	result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.readProximitySensor(s2)




	##################################################
	return distance
def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	s3 = sim.getObjectHandle('distance_sensor_3')
	result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.readProximitySensor(s3)



	##################################################
	return distance
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
			time.sleep(5)

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