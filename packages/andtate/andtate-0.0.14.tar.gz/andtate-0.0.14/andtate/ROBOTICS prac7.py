#################################### Practical 7 ######################################

import time
import random
directions = [10,30,90,60,40,28,32,64,11]
def move_forward():
    print("Moving forward")
    time.sleep(1)
def turn_left():
    print("Turning left")
    time.sleep(1)
def turn_right():
    print("Turning right")
    time.sleep(1)
def avoid_obstacle():
    if random.randint(0, 1) == 0:
        turn_left()
    else:
        turn_right()
def navigate():
	for i in directions:
            if i > 30:
                avoid_obstacle()
	    else:
		move_forward()
if __name__ == '__main__':
    navigate()
    print("Performed By NAME")