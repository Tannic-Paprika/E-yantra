'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi, Sairam Senapati, Raj Pattnaik, Ashish Kumar Sahu ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############

	for px in range(100,800,100):

		for py in range(100,800,100):

			intensity = maze_image[py,px]
			red = np.array([0,0,255])

			if (red == intensity).all() :

				position = str(chr(int((px/100) + 64)) + str(int(py/100)))
				traffic_signals += [position]
	
	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
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

	for px in range(150,750,100):

		for py in range(100,800,100):

			intensity = maze_image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				left_end = str(chr(int((px-50)/100) + 64) + str(int(py/100)))
				right_end = str(chr(int((px+50)/100) + 64) + str(int(py/100)))
				horizontal_roads_under_construction += [left_end + "-" + right_end]

	
	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

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
	for px in range(100,800,100):

		for py in range(150,750,100):

			intensity = maze_image[py,px]
			white = np.array([255,255,255])

			if (white == intensity).all() :

				upper_end = str(chr(int((px)/100) + 64) + str(int((py-50)/100)))
				lower_end = str(chr(int((px)/100) + 64) + str(int((py+50)/100)))
				vertical_roads_under_construction += [upper_end + "-" + lower_end]

	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

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
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############
	def shape_detection(No_of_sides): 

		if No_of_sides == 3 :
			return "Triangle"
		elif No_of_sides == 4 :
			return "Square"
		else:
			return "Circle"


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
		
	for px1 in range(105,705,100): #Accessing a particular shop

		shop_no = "Shop_" + str(int((px1-5)/100))
		shop_crop = maze_image[105:195 , px1:(px1+90)]
		gray = cv2.cvtColor(shop_crop, cv2.COLOR_BGR2GRAY)
		_,thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
		contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		shop_detail = []

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

		medicine_packages_present += shop_detail


	##################################################

	return medicine_packages_present

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

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
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############

	arena_parameters["traffic_signals"] = detect_traffic_signals(maze_image)

	arena_parameters["horizontal_roads_under_construction"] = detect_horizontal_roads_under_construction(maze_image)
	
	arena_parameters["vertical_roads_under_construction"] = detect_vertical_roads_under_construction(maze_image)

	arena_parameters["medicine_packages_present"] = detect_medicine_packages(maze_image)
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "/home/sree/Desktop/E-Yantra/PB_Task1_Ubuntu/Task1A/public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()
