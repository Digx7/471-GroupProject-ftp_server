import socket
import os
import sys

class Packet:
    def __init__(self, number, command, dataSize, data):
        self.number = number
        self.command = command
        self.dataSize = dataSize
        self.data = data

def recvData_as_bytes(sock, numBytes):

	# TODO: turn these empty string buffers into binary buffers

	# The buffer
	recvBuff = b""
	
	# The temporary buffer
	tmpBuff = b""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff

def recvPacket(sock):
    packetNumberBuffer = b""
    packetNumber = 0

    packetNumberBuffer = recvData_as_bytes(sock, 2)
    packetNumber = packetNumber.from_bytes(packetNumberBuffer)
    print ("Packet Number: ", packetNumber)

    packetCommandNameBuffer = b""
    commandName = ""

    packetCommandNameBuffer = recvData_as_bytes(sock, 6)
    commandName = packetCommandNameBuffer.decode()
    print ("Packet Command: " + commandName)

    packetDataSizeBuffer = b""
    dataSize = 0

    packetDataSizeBuffer = recvData_as_bytes(sock, 4)
    dataSize = dataSize.from_bytes(packetDataSizeBuffer)
    print ("Packet Data Size: ", dataSize)

    dataBuffer = b""

    if dataSize > 0:
        dataBuffer = recvData_as_bytes(sock, dataSize)
        print ("Data: ", dataBuffer)

    return Packet(packetNumber, commandName, dataSize, dataBuffer)

    # if commandName in responses_to_packets:
    #      responses_to_packets[commandName](packetNumber, dataBuffer)
    # else:
    #      respone_to_UnrecognizedPacket(dataBuffer)


def sendPacket(
        sock: socket, 
        packetNumber: bytes, 
        commandName: bytes, 
        dataSize: bytes, 
        data: bytes):
    packet = packetNumber + commandName + dataSize + data

    sock.send(packet)

def sendConnectPacket(
        sock: socket, 
        packetNumber: int,
        dataPortNumber: int):
    print("Sending Con")

    commandName = "000Con"

    data_as_bytes = dataPortNumber.to_bytes(4)

    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendConnectAcknowledgmentPacket(
        sock: socket, 
        packetNumber: int,
        dataPortNumber: int):
    print("Sending ConAck")

    commandName = "ConAck"

    data_as_bytes = dataPortNumber.to_bytes(4)

    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendDisconnectPacket(
        sock: socket, 
        packetNumber: int):
    print("Sending DisCon")

    commandName = "DisCon"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def sendGetPacket(
        sock: socket, 
        packetNumber: int,
        fileName: str):
    print("Sending Get")

    data_as_bytes = fileName.encode()

    commandName = "000Get"
    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)
    

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendPutPacket(
        sock: socket, 
        packetNumber: int,
        fileName: str):
    print("Sending Put")

    data_as_bytes = fileName.encode()

    commandName = "000Put"
    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendDeletePacket(
        sock: socket, 
        packetNumber: int,
        fileName: str):
    print("Sending Del")

    data_as_bytes = fileName.encode()

    commandName = "000Del"
    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendListRequestPacket(
        sock: socket, 
        packetNumber: int):
    print("Sending LsReq")

    commandName = "0LSReq"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def sendAcknowledgePacket(
        sock: socket, 
        packetNumber: int,
        packetToAcknowledge: int):
    print("Sending Ack")

    commandName = "000Ack"

    data_as_bytes = packetToAcknowledge.to_bytes(2)

    dataSize = len(data_as_bytes)

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)
    

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, data_as_bytes)

def sendInvalidPacket(
        sock: socket, 
        packetNumber: int):
    print("Sending InvPac")

    commandName = "InvPac"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def sendFileManifestPacket(
        sock: socket, 
        packetNumber: int):
    print("Sending FMan")

    commandName = "00FMan"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def sendFilePacket(
        sock: socket, 
        packetNumber: int):
    print("Sending File")

    commandName = "00File"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def sendFileStatusPacket(
        sock: socket, 
        packetNumber: int):
    print("Sending FStat")

    commandName = "0FStat"
    dataSize = 0

    packetNumber_as_bytes = packetNumber.to_bytes(2)
    commandName_as_bytes = commandName.encode()
    dataSize_as_bytes = dataSize.to_bytes(4)

    sendPacket(sock, packetNumber_as_bytes, commandName_as_bytes, dataSize_as_bytes, b'')

def isExpectedPacket(
        recivedPack: Packet,
        expectedPackName: str):
    if(recivedPack.command == expectedPackName):
        return True
    else:
        return False