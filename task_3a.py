'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1182 ]
# Author List:		[ Phanendra Sreeharsh Kowdodi , Sai Ram Senapati ]
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################





##############################################################

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
	# print(traffic_signals)
	##################################################

	return traffic_signals, start_node, end_node


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
	traffic_signals , start_node , end_node = detect_all_nodes(maze_image)
	paths = detect_paths_to_graph(maze_image)
	arena_parameters["traffic_signals"] = traffic_signals
	arena_parameters["start_node"] = start_node
	arena_parameters["end_node"] = end_node
	arena_parameters["paths"] = paths
	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	def dijkshtra_algo(graph,start,goal):
		shortest_distance = {}
		track_predecessor = {}
		unseenNodes = graph
		infinity = 100000 
		

		for node in unseenNodes:
			shortest_distance[node] = infinity
		shortest_distance[start] = 0
		# print(unseenNodes)
		while unseenNodes:
			min_distance_node = None 

			for node in unseenNodes :
				# print(node)
				if min_distance_node is None:
					min_distance_node = node
				elif shortest_distance[node] < shortest_distance[min_distance_node]:
					min_distance_node = node

			path_options = graph[min_distance_node].items()

			for child_node , weight in path_options:

				if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
					shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
					track_predecessor[child_node] = min_distance_node
			
			unseenNodes.pop(min_distance_node)

		currentNode = goal

		while currentNode != start :
			try:
				backtrace_path.insert(0,currentNode)
				currentNode = track_predecessor[currentNode]
			except KeyError:

				print("Path is not Reachable")
				break
		backtrace_path.insert(0,start)


	dijkshtra_algo(graph,start,end)
	##################################################


	return backtrace_path

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	facing = "up"
	for i in range(len(paths)-1) :
		
		current_node = paths[i]
		next_node = paths[i+1]

		current_node_letter = str(current_node[0])
		next_node_letter = str(next_node[0])

		current_node_number = int(current_node[1])
		next_node_number = int(next_node[1])


		if current_node in traffic_signal:
			list_moves += ["WAIT_5"]
		
		if current_node_letter != next_node_letter:
			
			if ord(next_node_letter) - ord(current_node_letter) > 0:
				if facing == "up":
					list_moves += ["RIGHT"]
					
				elif facing == "right":
					list_moves += ["STRAIGHT"]
					
				elif facing == "left":
					list_moves += ["REVERSE"]
				
				elif facing == "down":
					list_moves += ["LEFT"]
				
				facing = "right"

			else:
				if facing == "up":
					list_moves += ["LEFT"]
					
				elif facing == "right":
					list_moves += ["REVERSE"]
					
				elif facing == "left":
					list_moves += ["STRAIGHT"]
				
				elif facing == "down":
					list_moves += ["RIGHT"]
				
				facing = "left"
		
		elif current_node_number > next_node_number :
			if facing == "up":
				list_moves += ["STRAIGHT"]
					
			elif facing == "right":
				list_moves += ["LEFT"]
				
			elif facing == "left":
				list_moves += ["RIGHT"]
			
			elif facing == "down":
				list_moves += ["REVERSE"]
			
			facing = "up"
		else:
			
			if facing == "up":
				list_moves += ["REVERSE"]
				
			elif facing == "right":
				list_moves += ["RIGHT"]
				
			elif facing == "left":
				list_moves += ["LEFT"]
			
			elif facing == "down":
				list_moves += ["STRAIGHT"]
			
			facing = "down"
	##################################################

	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "D:/E-Yantra/PB_Task3A_Windows/test_images/"

	for file_num in range(0,10):
			
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )

			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()