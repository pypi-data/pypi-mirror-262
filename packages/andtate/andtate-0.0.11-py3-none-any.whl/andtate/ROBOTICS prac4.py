#################################### Practical 4 ######################################

import time
path = [(0,0),(0,1),(1,1),(2,3),(4,2),(5,1),(6,0)]
def moveTo(x,y):
    print('moving to', x, y)
    time.sleep(1)
def followPath(x,y):
    for point in path:
        moveTo(*point)
if __name__== '__main__':
    followPath(0,0)
print("performed by name")

