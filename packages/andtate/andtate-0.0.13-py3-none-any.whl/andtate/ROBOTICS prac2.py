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