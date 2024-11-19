# The server

# Needs to start up with
# pythonserv.py <PORTNUMBER> and then accepts requests at that port

# Valid commands
# pythonserv.py <PORTNUMBER>
# pythonserv.py help

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
#          respones_to_UnrecognizedPacket(packetNumber, dataBuffer)

def response_to_ConnectPacket(packetNumber: int, data: bytes):
    print ("recieved a connection packet")

    clientDataPortNumber.from_bytes(data)

    packet.sendConnectAcknowledgmentPacket(clientControlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(packetNumber: int, data: bytes):
    print ("recieved a connection acknowledgement packet")
    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_DisconnectPacket(packetNumber: int, data: bytes):
    print ("closing")

    # Close our side
    clientControlSock.close()
    controlSock.close()
    quit()

def response_to_GetPacket(packetNumber: int, data: bytes):
    print ("recieved a get packet")

    # TODO: check if file exists
    # If file exists open Data sock

    dataSock.bind(get_ip(), dataPortNumber)

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_PutPacket(packetNumber: int, data: bytes):
    print ("recieved a put packet")
    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_DeletePacket(packetNumber: int, data: bytes):
    print ("recieved a delete packet")
    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_ListRequestPacket(packetNumber: int, data: bytes):
    print ("recieved a list request packet")
    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

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

# Sets the port number that data will be recieved on
dataPortNumber = 300

clientDataPortNumber = 0

# Create a welcome socket. 
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
controlSock.bind((get_ip(), controlPortNumber))

# Start listening on the socket
controlSock.listen()

sockName = controlSock.getsockname()

print ("Waiting for connections...")
print (sockName)

# print(get_ip())


# Accept connections
clientControlSock, addr = controlSock.accept()

# TODO: get connection and do command

print ("Accepted connection from client: ", addr)
print ("\n")



while True:
    packet.recvPacket(clientControlSock, responses_to_packets, response_to_UnrecognizedPacket)
    