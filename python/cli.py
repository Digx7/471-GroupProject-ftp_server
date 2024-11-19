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

def setUp():
    expectPacket("ConAck")
    global runningProcedure
    runningProcedure = "SetUp"
    packet.sendConnectPacket(controlSock, 1, dataPortNumber)

# Downloads a file
def getFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Getting file: " + fileName)
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Get"
    packet.sendGetPacket(controlSock, 1, fileName)

# Uploads a file
def putFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Uploading file: " + fileName)
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Put"
    packet.sendPutPacket(controlSock, 1, fileName)

# Deletes a file
def deleteFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Deleting file: " + fileName)
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Delete"
    packet.sendDeletePacket(controlSock, 1, fileName)

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
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "List"
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



def response_to_ConnectPacket(recieved: packet.Packet):
    print ("recieved a connection packet")

    serverDataPortNumber.from_bytes(recieved.data)

    packet.sendConnectAcknowledgmentPacket(controlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(recieved: packet.Packet):
    print ("recieved a connection acknowledgement packet")

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    notExpectingPacket()

    packet.sendAcknowledgePacket(controlSock, 1, packetNumber)

def response_to_DisconnectPacket(recieved: packet.Packet):
    print ("closing")

def response_to_GetPacket(recieved: packet.Packet):
    print ("recieved a get packet")

def response_to_PutPacket(recieved: packet.Packet):
    print ("recieved a put packet")

def response_to_DeletePacket(recieved: packet.Packet):
    print ("recieved a delete packet")

def response_to_ListRequestPacket(recieved: packet.Packet):
    print ("recieved a list request packet")

def response_to_AcknowledgePacket(recieved: packet.Packet):
    print ("recieved a acknowledge packet")
    notExpectingPacket()

def response_to_InvalidPacket(recieved: packet.Packet):
    print ("recieved a invalid packet")

def response_to_FileManifestPacket(recieved: packet.Packet):
    print ("recieved a file manifest packet")

def response_to_FilePacket(recieved: packet.Packet):
    print ("recieved a file packet")

def response_to_FileStatusPacket(recieved: packet.Packet):
    print ("recieved a file status packet")

def response_to_UnrecognizedPacket(recieved: packet.Packet):
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

def respondToPacket(packet: packet.Packet):
    if packet.command in responses_to_packets:
        responses_to_packets[packet.command](packet)
    else:
        response_to_UnrecognizedPacket(packet)

def expectPacket(command: str):
    global isExpectingPacket
    global expectedPacketName

    isExpectingPacket = True
    expectedPacketName = command

def notExpectingPacket():
    global isExpectingPacket

    isExpectingPacket = False

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

# Procedures
isExpectingPacket = False
expectedPacketName = ""

runningProcedure = ""
procedureStep = 0

def sendFMan(recived: packet.Packet):
    packet.sendFileManifestPacket(controlSock, 1)

def sendGet(recived: packet.Packet):
    packet.sendGetPacket(controlSock, 1, "Name")

allProcedures = {
    "SetUp" : (["ConAck"],[response_to_ConnectAcknowledmentPacket]),
    "Get" : (["000Ack", "000Ack", "000Ack"],[ sendFMan, sendGet, response_to_AcknowledgePacket])
}

# packet.sendConnectPacket(controlSock, 1, dataPortNumber)
setUp()
# if(isExpectingPacket):
#     print("Expecting packet")
#     lastPacket = packet.recvPacket(controlSock)
#     if(packet.isExpectedPacket(lastPacket, expectedPacketName)):
#         respondToPacket(lastPacket)

dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def buildControlSock():
    # Creates a control socket
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    controlSock.connect((serverMachineAddress, serverControlPortNumber))

print("Connecting to the server")

while True:

    if(runningProcedure != ""):
        # a procedure is running

        procedureExpectedPackets, procedureResponses = allProcedures[runningProcedure]

        if procedureStep < len(procedureExpectedPackets):
            lastPacket = packet.recvPacket(controlSock)
            if(packet.isExpectedPacket(lastPacket, procedureExpectedPackets[procedureStep])):
                procedureResponses[procedureStep](lastPacket)
                procedureStep += 1
        else:
            runningProcedure = ""
            procedureStep = 0
    else:


        print ("ftp>", end =" ")

        inputRaw = input()

        inputArgs = list(map(str, inputRaw.split(' ')))

        if inputArgs[0] in ftpCommands:
            ftpCommands[inputArgs[0]](inputArgs)
        else:
            errorFTPCommand(inputArgs)

