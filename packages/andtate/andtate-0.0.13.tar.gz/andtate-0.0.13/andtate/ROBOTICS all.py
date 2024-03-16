####################################Practical 1 ######################################
1. Open Terminal and enter below command:
sudo raspi-config

Select Interface Options from the menu
Select ssh enable/disable remote command line access using ssh.
Select Yes to enable ssh server

2.Check the ip address of raspberry pi using below command:
$ ip a

3.Check if the service is running using below command:
sudo systemctl status sshd

4.Open putty on another computer within same network and enter raspberry pi ip address:

5.It will ask for username and password of pi user:
Enter username and password respectively.
####################################Practical 2 ######################################
1. Check ip address of raspberry pi using below command.
ip a

2.Create a file to be uploaded on raspberry pi (piUpload.txt)

3.ping 192.168.176.129 (It should be successful)

4.open cmd in another system in same network and start connecting to sftp:
a.) first go to directory where file is created:
cd D:\Documents\piUpload

b.) connect to raspberry pi sftp and enter password:
sftp <username>@<ip-address>
sftp pi@192.168.176.129

c.) check currect directory of pi.
pwd (it will return current pi directory)
we can check there is no file in pi on given path.

d.) now upload file to pi using below command:
put <filename>
put piUpload.txt



####################################Practical 3 ######################################
https://www.tinkercad.com/things/6kz72ezIC46-pract-3

#include <Servo.h>
Servo myservo;
int potpin = 0;
int val;
void setup() {
    myservo.attach(9);
}
void loop() {
    val = analogRead(potpin);
    val = map(val, 0, 1023, 0, 180);
    myservo.write(val);
    delay(15);
}


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

#################################### Practical 5B ######################################
https://www.tinkercad.com/things/9x8AvKWmhgm-pract-5

#include <LiquidCrystal.h>
LiquidCrystal lcd(1, 2, 4, 5, 6, 7);
int celsius = 0;
void setup() {
    lcd.begin(16,2);
}
void loop() {
    celsius = map(((analogRead(A0) - 20) * 3.04), 0, 1023, -40, 125);
    lcd.print("Name");
    lcd.setCursor(0,1);
    lcd.print(celsius);
    delay(4000);
    lcd.clear();
}

#################################### Practical 6 ######################################
https://www.tinkercad.com/things/21OM6rBLsUA-pract-6

#include <Adafruit_NeoPixel.h>
#define PIN 2
#define NUMPIXELS 12
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB +
NEO_KHZ800);
int delayval = 100;
int redColor = 0;
int greenColor = 0;
int blueColor = 0;
void setup() {
    pixels.begin();
}
void loop() {
    redColor = random(0, 255);
    greenColor = random(0,255);
    blueColor = random(0, 255);
    for (int i=0; i < NUMPIXELS; i++) {
        pixels.setPixelColor(i, pixels.Color(redColor, greenColor, blueColor));
        pixels.show();
        delay(delayval);
    }
}



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

#################################### Practical 8 ######################################


import numpy as np
import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
'haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
'haarcascade_eye.xml')
img = cv2.imread('image.jpeg')
cv2.imshow('Original',img)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
cv2.imshow('output',img)
