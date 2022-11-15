from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""
signed_silver_list = []
signed_gold_list = [] 

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token(token_type):
    """
    Function to find the closest token that the robot can see of the type passed as parameter (MARKER_TOKEN_SILVER or MARKER_TOKEN_GOLD) and that has not already been used

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	code : the numeric code of the closest token that the robot can see and that has not already been used (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
    	if token.info.marker_type == token_type:
		if token.dist < dist and ((not (token.info.code in signed_silver_list) and token.info.marker_type==MARKER_TOKEN_SILVER) or (not (token.info.code in signed_gold_list) and token.info.marker_type==MARKER_TOKEN_GOLD)) :
		    dist=token.dist
		    rot_y=token.rot_y
		    code = token.info.code
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, code


def grab_token():
	"""
	This function is used to go near the token returned by the function find_token() and grab it
	"""
	while 1:
	    dist, rot_y, code = find_token(MARKER_TOKEN_SILVER)  # we look for silver tokens
	    if dist==-1:
		print("I don't see any token!!")
		turn(20, 0.5)  # if no silver tokens are detected, turns to find
	    elif dist <d_th: 
		print("Found it!")
		if R.grab(): # if we are close to the token, we grab it.
			signed_silver_list.append(code) # after grab it we write its code inside a list to avoid to grab it twice
			print("Gotcha!")
			return 
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(30, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)

def get_close_gold():
	"""
	This function is used to go near the token returned by the function find_token() and release the silver one next to it
	"""
	while 1:
	    dist, rot_y, code = find_token(MARKER_TOKEN_GOLD)  # we look for gold tokens
	    if dist==-1:
		print("I don't see any token!!")
		turn(20, 0.5)  # if no gold tokens are detected, turns to find
	    elif dist <1.5*d_th: 
		print("Found it!")
		if R.release(): # if we are close to the token, we release the silver one.
			signed_gold_list.append(code) # after release the silver one we write the code of the gold one inside a list to avoid to release a silver token next to it twice
			print("Gotcha!")
			return 
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(30, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)
		
while 1:
	"""
	The main consists in a loop that calls the functions written above and this loop ends when all the tokens are paired
	"""
 
	grab_token()
	get_close_gold()
	drive(-20, 1)
	if len(signed_gold_list) == 6:
		print("ALL THE TOKENS HAVE BEEN CORRECTLY PAIRED")
		exit()


 
