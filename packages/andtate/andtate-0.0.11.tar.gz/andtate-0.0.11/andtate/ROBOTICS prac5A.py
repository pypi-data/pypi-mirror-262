#################################### Practical 5A ######################################

import time
import random
def read_sensor():
type of sensor being used
    return random.uniform(0, 1) # placeholder random value
def test_sensor():
    for i in range(10):
        data = read_sensor()
	print(f"Reading {i + 1}: {data}")
	time.sleep(1)
if __name__ == '__main__':
    test_sensor()
    print("Performed By NAME")
