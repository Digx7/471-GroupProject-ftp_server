# The client

# Needs to start up with
# cli.py <server machine> <server port>

# It then connects to the server and begins pringing out
# ftp> where the user can type in the following commands
# ftp> get <file name>
# ftp> put <file name>
# ftp> delete <file name>
# ftp> help
# ftp> ls
# ftp> quit

import socket
import os
import sys

# Check if the help command was input
if len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "h":
        print ("This is the python client script for a simple ftp server")
        print ("To setup the client first make sure the server is running")
        print ("Next run the following command:")
        print (sys.argv[0] + " <server machine> <server port>")
        print ("To see this message again use the following command")
        print (sys.argv[0] + " help")
        quit()
    else:
        print ("Inteded usage: " + sys.argv[0] + " <server machine> <server port>")
        quit()

# Check number of command line args
if len(sys.argv) != 3:
    print ("Inteded usage: " + sys.argv[0] + " <server machine> <server port>")
    quit()

# Gets arguments
serverMachineAddress = str(sys.argv[1])
serverControlPortNumber = int(sys.argv[2])

# TODO: connect to the server

# Creates a control socket
# controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
# controlSock.connect((serverMachineAddress, serverControlPortNumber))

# All the ftp commands availble once the connection is set

# Downloads a file
def getFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Getting file: " + fileName)

# Uploads a file
def putFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Uploading file: " + fileName)

# Deletes a file
def deleteFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Deleting file: " + fileName)

# Lists out all valid commands
def helpFTPCommand(inputArgs):
    print("Valid commands:")
    print("get <FILENAME>")
    print("put <FILENAME>")
    print("delete <FILENAME>")
    print("ls")
    print("help")
    print("quit\n")

# Lists out all files on FTP server
def lsFTPCommand(inputArgs):
    print("Listing file names")

# Quits execution
def quitFTPCommand(inputArgs):
    print("Goodbye!")
    quit()

# Runs if the command is not recognized
def errorFTPCommand(inputArgs):
    print("Invalid command")
    print("Use the help command to see all valid commands")

# Dictionary of all ftp commands
ftpCommands = {
    "get" : getFTPCommand,
    "put" : putFTPCommand,
    "delete" : deleteFTPCommand,
    "help" : helpFTPCommand,
    "ls" : lsFTPCommand,
    "quit" : quitFTPCommand
}


print ("TODO: implement to the server, we'll just fake it for now")

while True:

    print ("ftp>", end =" ")

    inputRaw = input()

    inputArgs = list(map(str, inputRaw.split(' ')))

    if inputArgs[0] in ftpCommands:
        ftpCommands[inputArgs[0]](inputArgs)
    else:
        errorFTPCommand(inputArgs)

