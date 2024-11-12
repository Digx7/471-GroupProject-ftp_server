# The server

# Needs to start up with
# pythonserv.py <PORTNUMBER> and then accepts requests at that port

# Valid commands
# pythonserv.py <PORTNUMBER>
# pythonserv.py help

import socket
import os
import sys


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
controlSock.bind(('', controlPortNumber))

# Start listening on the socket
controlSock.listen(1)

while True:

    print ("Waiting for connections...")

    # Accept connections
    clientControlSock, addr = controlSock.accept()

    # TODO: get connection and do command

    print ("Accepted connection from client: ", addr)
    print ("\n")

    # Close our side
    clientControlSock.close()