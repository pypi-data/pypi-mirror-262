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