'''
*****************************************************************************************
*
*        		     ===============================================
*           		       Pharma Bot (PB) Theme (eYRC 2022-23)
*        		     ===============================================
*
*  This script contains all the past implemented functions of Pharma Bot (PB) Theme 
*  (eYRC 2022-23).
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi , Ashish Kumar Sahu ,  Sai Ram Senapati ]
# Filename:			PB_theme_functions.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
from zmqRemoteApi import RemoteAPIClient
import traceback
import zmq
import numpy as np
import cv2
from pyzbar.pyzbar import decode
import json
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################


##############################################################


################## ADD SOCKET COMMUNICATION ##################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 3D for setting up a Socket
Communication Server in this section
"""

def setup_server(host, port):

	"""
	Purpose:
	---
	This function creates a new socket server and then binds it 
	to a host and port specified by user.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`server` : [ socket object ]
	---

	
	Example call:
	---
	server = setupServer(host, port)
	""" 

	server = None

	##################	ADD YOUR CODE HERE	##################
	server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((host,port))

	##########################################################

	return server

def setup_connection(server):
	"""
	Purpose:
	---
	This function listens for an incoming socket client and
	accepts the connection request

	Input Arguments:
	---
	`server` :	[ socket object ]
			socket object created by setupServer() function
	Returns:
	---
	`server` : [ socket object ]
	
	Example call:
	---
	connection = setupConnection(server)
	"""
	connection = None
	address = None

	##################	ADD YOUR CODE HERE	##################
	server.listen(10)

	connection,address= server.accept()	

	##########################################################

	return connection, address

def receive_message_via_socket(connection):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################
	message = connection.recv(1024)
	message_decode = message.decode()

	##########################################################

	return message

def send_message_via_socket(connection, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`connection` :	[ connection object ]
			connection object created by setupConnection() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################
	message_encode= message.encode(encoding = 'UTF-8')
	connection.send(message_encode)

	##########################################################

##############################################################
##############################################################

######################### ADD TASK 2B ########################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 2B for reading QR code from
CoppeliaSim arena in this section
"""

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the CoppeliaSim vision sensor's 
	field of view and returns the message encoded into it.

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
	def get_vision_data(sim):

		visionSensorHandle = sim.getObjectHandle('vision_sensor')
		img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)  #Capturing image from sensor
		img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)		
		img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0) 

	img= get_vision_data(sim)
	barcodes = decode(img)
	bdata= barcodes[0].data.decode("utf-8")
	qr_message= f"{bdata}"

	##################################################

	return qr_message

##############################################################
##############################################################

############### ADD ARENA PARAMETER DETECTION ################


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}

	##############	ADD YOUR CODE HERE	##############
	for px in range(100,700,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			intensity_right = image[py,px+15]
			intensity_left = image[py,px-15]
			intensity_below = image[py+15,px]
			intensity_above = image[py-15,px]

			black = np.array([0,0,0])

			position = str(chr(int((px/100) + 64)) + str(int(py/100)))
			
			position_list={}
			

			if (intensity_right == black).all() :
				position_right = str(chr(int((px/100) + 64 + 1)) + str(int(py/100)))
				position_list[position_right] = 1

			if (intensity_left == black).all() :
				position_left = str(chr(int((px/100) + 64 - 1)) + str(int(py/100)))
				position_list[position_left] = 1
			
			if (intensity_above == black).all() :
				position_above = str(chr(int((px/100) + 64 )) + str(int(py/100)-1))
				position_list[position_above] = 1

			if (intensity_below == black).all() :
				position_below = str(chr(int((px/100) + 64 )) + str(int(py/100)+1))
				position_list[position_below] = 1
			# position = str(chr(int((px/100) + 64)) + str(int(py/100)))
			paths[position]=position_list
	# print(paths)
	##################################################

	return paths

####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 1A and 3A for detecting arena parameters
from configuration image in this section
"""

def detect_all_nodes(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals, start_node and end_node are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals, start_node, end_node` : [ list ], str, str
			list containing nodes in which traffic signals are present, start and end node too
	
	Example call:
	---
	traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
	"""    
	traffic_signals = []
	start_node = ""
	end_node = ""

    ##############	ADD YOUR CODE HERE	##############
	for px in range(100,700,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			red = np.array([0,0,255])
			green = np.array([0,255,0])
			purple = np.array([189,43,105])

			if (intensity == green).all():
				start_node = str(chr(int((px/100) + 64)) + str(int(py/100)))

			if (intensity == purple).all():
				end_node = str(chr(int((px/100) + 64)) + str(int(py/100)))

			if (intensity == red).all() :

				position = str(chr(int((px/100) + 64)) + str(int(py/100)))
				traffic_signals += [position]

    ##################################################

	return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(image):	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for px in range(150,650,100):

		for py in range(100,700,100):

			intensity = image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				left_end = str(chr(int((px-50)/100) + 64) + str(int(py/100)))
				right_end = str(chr(int((px+50)/100) + 64) + str(int(py/100)))
				horizontal_roads_under_construction += [left_end + "-" + right_end]

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	for px in range(100,700,100):

		for py in range(150,650,100):

			intensity = image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				upper_end = str(chr(int((px)/100) + 64) + str(int((py-50)/100)))
				lower_end = str(chr(int((px)/100) + 64) + str(int((py+50)/100)))
				vertical_roads_under_construction += [upper_end + "-" + lower_end]
	
	##################################################
	
	return vertical_roads_under_construction

def detect_medicine_packages(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############
	def shape_detection(No_of_sides): 

		if No_of_sides == 3 :
			return "cone"
		elif No_of_sides == 4 :
			return "cube"
		else:
			return "cylinder"


	def detect_colour(pixel_value):

		Green = np.array([0,255,0])
		Pink = np.array([180,0,255])
		Skyblue = np.array([255 ,255,0])
		Orange = np.array([0,127,255])
		if (pixel_value == Green).all() :
			return "Green"
		elif (pixel_value == Pink).all() :
			return "Pink"
		elif (pixel_value == Orange).all() :
			return "Orange"
		elif (pixel_value == Skyblue).all() :
			return "Skyblue"
		
	for px1 in range(105,605,100): #Accessing a particular shop

		shop_no = "Shop_" + str(int((px1-5)/100))
		shop_crop = image[105:195 , px1:(px1+90)]
		gray = cv2.cvtColor(shop_crop, cv2.COLOR_BGR2GRAY)
		_,thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		shop_detail = []
		contours = list(contours)
		if len(contours) != 1: #Rejecting the empty shops
			
			contours.pop(0)  #Removing the boundary of cropped image contour

			for contour in contours: #INSIDE A SHAPE

				shape_detail = [] #All Info of a particular shape
				approx = cv2.approxPolyDP(contour,0.02*cv2.arcLength(contour,True),True)
				shape = shape_detection(len(approx))
				M = cv2.moments(contour)
				if M['m00'] != 0:
					cx = int(M['m10']/M['m00']) 
					cy = int(M['m01']/M['m00'])
				shape_detail += [shop_no , detect_colour(shop_crop[cy,cx]) , shape , [cx + px1 ,cy + 105]]
				shop_detail += [shape_detail]
			shop_detail.sort(key = lambda x : x[1]) #Sorting as per Colour

		medicine_packages += shop_detail

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
	arena_parameters["traffic_signals"] , arena_parameters["start_node"] , arena_parameters["end_node"] = detect_all_nodes(maze_image)

	arena_parameters["paths"]=detect_paths_to_graph(maze_image)
    ##################################################

	return arena_parameters

##############################################################
##############################################################

####################### ADD ARENA SETUP ######################
####################### FUNCTIONS HERE #######################
"""
Add functions written in Task 4A for setting up the CoppeliaSim
Arena according to the configuration image in this section
"""

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    

####################### ADD YOUR CODE HERE #########################

    shops = {"Shop_1":[] , "Shop_2":[] ,"Shop_3":[] ,"Shop_4":[] ,"Shop_5":[]  }
    
    for package in medicine_package_details:
        
        if package[0] == "Shop_1":
            shops["Shop_1"] += [package]
        
        elif package[0] == "Shop_2":
            shops["Shop_2"] += [package]

        elif package[0] == "Shop_3":
            shops["Shop_3"] += [package]

        elif package[0] == "Shop_4":
            shops["Shop_4"] += [package]  

        elif package[0] == "Shop_5":
            shops["Shop_5"] += [package]  


    y_shop = -0.695
    ######  SHOP 1 ######  
    # x_shop = 0.84
    z = 0.015
    if len(shops["Shop_1"]) != 0:

        package_no = 1
        for package in shops["Shop_1"]:
            # print(package)
            x_shop = 0.84 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ######  SHOP 2 ######
    if len(shops["Shop_2"]) != 0:
        package_no = 1
        for package in shops["Shop_2"]:
            # print(package)
            x_shop = 0.48 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 3 ######
    if len(shops["Shop_3"]) != 0:
        package_no = 1
        for package in shops["Shop_3"]:
            # print(package)
            x_shop = 0.12 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 4 ######
    if len(shops["Shop_4"]) != 0:
        package_no = 1
        for package in shops["Shop_4"]:
            # print(package)
            x_shop = -0.24 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

    ###### SHOP 5 ######
    if len(shops["Shop_5"]) != 0:
        package_no = 1
        for package in shops["Shop_5"]:
            # print(package)
            x_shop = -0.60 - (package_no-1)*(0.08)
            package_no+=1
            package_name = package[1]+"_" + package[2]
            package_path = packages_models_directory+ "\\" + package_name+".ttm" 
            # print(package_path)
            # print(x_shop,"is x of shop")
            objectHandle = sim.loadModel(package_path)
            sim.setObjectParent(objectHandle,arena,False)
            sim.setObjectAlias(objectHandle,package_name)
            sim.setObjectPosition(objectHandle,-1,[x_shop,y_shop,z])
            all_models+=[objectHandle]

####################################################################

    return all_models

def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
    
    for signal in traffic_signals:
        
        x = 0.90 - (ord(signal[0])-65)*0.36
        y = -0.90 + (int(signal[1])-1)*0.36
        objectHandle = sim.loadModel(traffic_sig_model)
        sim.setObjectParent(objectHandle,arena,False)
        sim.setObjectAlias(objectHandle,"Signal_"+signal)
        sim.setObjectPosition(objectHandle,-1,[x,y,0.15588])
        all_models+=[objectHandle]

####################################################################

    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   

####################### ADD YOUR CODE HERE #########################
	# print(start_node , "is start node")
    # print(end_node , "is end node")

    x_start = 0.90 - (ord(start_node[0])-65)*0.36
    y_start = -0.90 + (int(start_node[1])-1)*0.36

    x_end = 0.90 - (ord(end_node[0])-65)*0.36
    y_end = -0.90 + (int(end_node[1])-1)*0.36

    objectHandle_start = sim.loadModel(start_node_model)
    sim.setObjectParent(objectHandle_start,arena,False)
    sim.setObjectAlias(objectHandle_start,"Start_Node")

    objectHandle_end = sim.loadModel(end_node_model)
    sim.setObjectParent(objectHandle_end,arena,False)
    sim.setObjectAlias(objectHandle_end,"End_Node")


    sim.setObjectPosition(objectHandle_start,-1,[x_start,y_start,0.15588])
    all_models+=[objectHandle_start]

    sim.setObjectPosition(objectHandle_end,-1,[x_end,y_end,0.15588])
    all_models+=[objectHandle_end]
    

####################################################################

    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  

####################### ADD YOUR CODE HERE #########################
	# print(horizontal_roads_under_construction)
    for road in horizontal_roads_under_construction:

        barri_x = ord(road[0])
        barri_x = 0.72 - (barri_x-65)*0.36
        # print(barri_x-65)
        
        barri_y = -0.90 + (int(road[1])-1)*0.36

        # print(barri_x,"is x")
        # print(barri_y,"is y")
#  Horizontal_missing_node_D5_E5
        objectHandle_barri = sim.loadModel(horiz_barricade_model)
        sim.setObjectParent(objectHandle_barri,arena,False)
        sim.setObjectAlias(objectHandle_barri,"Horizontal_missing_road_"+road)

        sim.setObjectPosition(objectHandle_barri,-1,[barri_x,barri_y,0.024])

        all_models+=[objectHandle_barri]


####################################################################

    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena')

####################### ADD YOUR CODE HERE #########################
	 # print(vertical_roads_under_construction)
    for road in vertical_roads_under_construction:

        barri_x = 0.90 - (ord(road[0])-65)*0.36
        
        # barri_x = 0.72 - (barri_x-65)*0.36
        # print(barri_x-65)
        barri_y = int(road[4])
        barri_y = -0.72 + (barri_y -2)*0.36

        # print(barri_x,"is x")
        # print(barri_y,"is y")

        objectHandle_barri = sim.loadModel(vert_barricade_model)
        sim.setObjectParent(objectHandle_barri,arena,False)
        sim.setObjectAlias(objectHandle_barri,"Vertical_missing_road_"+road)

        sim.setObjectPosition(objectHandle_barri,-1,[barri_x,barri_y,0.024])
        
        all_models+=[objectHandle_barri]

####################################################################

    return all_models

##############################################################
##############################################################