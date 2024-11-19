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
import packet

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip



# All the ftp commands availble once the connection is set

# Downloads a file
def getFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Getting file: " + fileName)
    packet.sendGetPacket(controlSock, 1)

# Uploads a file
def putFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Uploading file: " + fileName)
    packet.sendPutPacket(controlSock, 1)

# Deletes a file
def deleteFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Deleting file: " + fileName)
    packet.sendDeletePacket(controlSock, 1)

# Lists out all valid commands
def helpFTPCommand(inputArgs):
    print("Valid commands:")
    print("get <FILENAME>")
    print("put <FILENAME>")
    print("delete <FILENAME>")
    print("ls")
    print("help")
    print("quit")
    print("exit")

# Lists out all files on FTP server
def lsFTPCommand(inputArgs):
    print("Listing file names")
    packet.sendListRequestPacket(controlSock, 1)

# Quits execution
def quitFTPCommand(inputArgs):
    print("Goodbye!")
    packet.sendDisconnectPacket(controlSock, 1)
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
    "quit" : quitFTPCommand,
    "exit" : quitFTPCommand
}


# def recvData_as_bytes(sock, numBytes):

# 	# TODO: turn these empty string buffers into binary buffers

# 	# The buffer
# 	recvBuff = b""
	
# 	# The temporary buffer
# 	tmpBuff = b""
	
# 	# Keep receiving till all is received
# 	while len(recvBuff) < numBytes:
		
# 		# Attempt to receive bytes
# 		tmpBuff =  sock.recv(numBytes)
		
# 		# The other side has closed the socket
# 		if not tmpBuff:
# 			break
		
# 		# Add the received bytes to the buffer
# 		recvBuff += tmpBuff
	
# 	return recvBuff

# def recvPacket(sock):
#     packetNumberBuffer = b""
#     packetNumber = 0

#     packetNumberBuffer = recvData_as_bytes(sock, 2)
#     packetNumber = packetNumber.from_bytes(packetNumberBuffer)
#     print ("Packet Number: ", packetNumber)

#     packetCommandNameBuffer = b""
#     commandName = ""

#     packetCommandNameBuffer = recvData_as_bytes(sock, 6)
#     commandName = packetCommandNameBuffer.decode()
#     print ("Packet Command: " + commandName)

#     packetDataSizeBuffer = b""
#     dataSize = 0

#     packetDataSizeBuffer = recvData_as_bytes(sock, 4)
#     dataSize = dataSize.from_bytes(packetDataSizeBuffer)
#     print ("Packet Data Size: ", dataSize)

#     dataBuffer = b""

#     if dataSize > 0:
#         dataBuffer = recvData_as_bytes(sock, dataSize)
#         print ("Data: " + dataBuffer)

#     if commandName in responses_to_packets:
#          responses_to_packets[commandName](dataBuffer)
#     else:
#          respones_to_UnrecognizedPacket(dataBuffer)


def response_to_ConnectPacket(packetNumber: int, data: bytes):
    print ("recieved a connection packet")

    serverDataPortNumber = serverDataPortNumber.from_bytes(data)

    packet.sendConnectAcknowledgmentPacket(controlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(packetNumber: int, data: bytes):
    print ("recieved a connection acknowledgement packet")
    packet.sendAcknowledgePacket(controlSock, 1, packetNumber)

def response_to_DisconnectPacket(packetNumber: int, data: bytes):
    print ("closing")

def response_to_GetPacket(packetNumber: int, data: bytes):
    print ("recieved a get packet")

def response_to_PutPacket(packetNumber: int, data: bytes):
    print ("recieved a put packet")

def response_to_DeletePacket(packetNumber: int, data: bytes):
    print ("recieved a delete packet")

def response_to_ListRequestPacket(packetNumber: int, data: bytes):
    print ("recieved a list request packet")

def response_to_AcknowledgePacket(packetNumber: int, data: bytes):
    print ("recieved a acknowledge packet")

def response_to_InvalidPacket(packetNumber: int, data: bytes):
    print ("recieved a invalid packet")

def response_to_FileManifestPacket(packetNumber: int, data: bytes):
    print ("recieved a file manifest packet")

def response_to_FilePacket(packetNumber: int, data: bytes):
    print ("recieved a file packet")

def response_to_FileStatusPacket(packetNumber: int, data: bytes):
    print ("recieved a file status packet")

def response_to_UnrecognizedPacket(packetNumber: int, data: bytes):
     print ("error: recieved unrecognized packet")

responses_to_packets = {
     "000Con" : response_to_ConnectPacket,
     "ConAck" :  response_to_ConnectAcknowledmentPacket,
     "DisCon" : response_to_DisconnectPacket,
     "000Get" : response_to_GetPacket,
     "000Put" : response_to_PutPacket,
     "000Del" : response_to_DeletePacket,
     "0LSReq" : response_to_ListRequestPacket,
     "000Ack" : response_to_AcknowledgePacket,
     "InvPac" : response_to_InvalidPacket,
     "00FMan" : response_to_FileManifestPacket,
     "00File" : response_to_FilePacket,
     "0FStat" : response_to_FileStatusPacket,
}

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

# Sets the port number that data will be recieved on
dataPortNumber = 200

serverDataPortNumber = 0

# Creates a control socket
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
controlSock.connect((serverMachineAddress, serverControlPortNumber))

packet.sendConnectPacket(controlSock, 1, dataPortNumber)
packet.recvPacket(controlSock, responses_to_packets, response_to_UnrecognizedPacket)

dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def buildControlSock():
    # Creates a control socket
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    controlSock.connect((serverMachineAddress, serverControlPortNumber))

print("Connecting to the server")

while True:

    print ("ftp>", end =" ")

    inputRaw = input()

    inputArgs = list(map(str, inputRaw.split(' ')))

    if inputArgs[0] in ftpCommands:
        ftpCommands[inputArgs[0]](inputArgs)
    else:
        errorFTPCommand(inputArgs)
    
    packet.recvPacket(controlSock, responses_to_packets, response_to_UnrecognizedPacket)

