# The server

# Needs to start up with
# pythonserv.py <PORTNUMBER> and then accepts requests at that port

# Valid commands
# pythonserv.py <PORTNUMBER>
# pythonserv.py help

import socket
import os
import sys

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Check number of command line args
if len(sys.argv) != 2:
    print ("Inteded usage: pythonserv.py <PORTNUMBER>")
    quit()

# Checks if the help argument was passed
if sys.argv[1] == "help" or sys.argv[1] == "h":
    print("This is the python server script for a simple ftp server")
    print("To set the server up run the following command")
    print("python pythonserv.py <PORTNUMBER>")
    print("To see this message again just type")
    print("python pythonserv.py help")
    quit()

# Sets the main control port to list to
controlPortNumber = int(sys.argv[1])

# Create a welcome socket. 
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
controlSock.bind((get_ip(), controlPortNumber))

# Start listening on the socket
controlSock.listen(1)

sockName = controlSock.getsockname()


while True:

    print ("Waiting for connections...")
    print (sockName)

    # print(get_ip())


    # Accept connections
    clientControlSock, addr = controlSock.accept()

    # TODO: get connection and do command

    print ("Accepted connection from client: ", addr)
    print ("\n")

    print ("closing")

    # Close our side
    clientControlSock.close()
    controlSock.close()
    quit()