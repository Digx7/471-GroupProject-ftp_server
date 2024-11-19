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
import procedures

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
    # packet.sendGetPacket(controlSock, 1)
    procedureManager.startProcedure("Get")

# Uploads a file
def putFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Uploading file: " + fileName)
    # packet.sendPutPacket(controlSock, 1)
    procedureManager.startProcedure("Put")

# Deletes a file
def deleteFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("a file name is needed")
        return
    fileName = inputArgs[1]
    print("Deleting file: " + fileName)
    # packet.sendDeletePacket(controlSock, 1)
    procedureManager.startProcedure("Delete")

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
    # packet.sendListRequestPacket(controlSock, 1)
    procedureManager.startProcedure("List")

# Quits execution
def quitFTPCommand(inputArgs):
    print("Goodbye!")
    # packet.sendDisconnectPacket(controlSock, 1)
    procedureManager.startProcedure("Quit")
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


# Responses to packets

def response_to_ConnectPacket(packetNumber: int, data: bytes):
    print ("recieved a connection packet")

    serverDataPortNumber.from_bytes(data)

    packet.sendConnectAcknowledgmentPacket(controlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(packetNumber: int, data: bytes):
    print ("recieved a connection acknowledgement packet")

    serverDataPortNumber.from_bytes(data)

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

# Building socks

def buildControlSock():
    # Creates a control socket
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    controlSock.connect((serverMachineAddress, serverControlPortNumber))

def connectDataSock():
    print("Attemting to connect data sock")
    
    dataSock.connect((serverMachineAddress, serverDataPortNumber))
    packet.sendConnectPacket(dataSock, 1, dataPortNumber)
    packet.recvPacket(dataSock, responses_to_packets, response_to_UnrecognizedPacket)

def connectSock(sock: socket.socket, address, port):
    sock.connect((address, port))
    packet.sendConnectPacket(sock, 1, dataPortNumber)
    packet.recvPacket(sock, responses_to_packets, response_to_UnrecognizedPacket)

def lastPacketIsAck(packet):
    print("Checking if the last packet is Ack")
    if packet.command == "000Ack":
        return 100
    else:
        return 200

def lastPackIsControlAck(packet):
    print("Checking if the last packet is ConAck")
    if packet.command == "ConAck":
        serverDataPortNumber.from_bytes(packet.data)
        return 100
    else:
        return 200

def execute_withValue(value):
    print(value) 
    print("Executing step")

def execute():
    print("Executing step")

def validate():
    return 100

def passed():
    print("step passed")

def error1():
    print("Error 1")

def error2():
    print("Error 2")

def allOtherErrors():
    print("Error N")

# myProcedure1 = packet.Procedure()
# myProcedure1.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# myProcedure1.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# myProcedure1.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# myProcedure1.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)

# myProcedure2 = packet.Procedure()
# myProcedure2.buildStep(lambda: execute_withValue(value="I did something"), passed, error1, error2, allOtherErrors)
# myProcedure2.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# myProcedure2.buildStep(lambda: execute_withValue(value="I did another thing"), passed, error1, error2, allOtherErrors)
# myProcedure2.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)

# myProcedure3 = packet.Procedure()
# myProcedure3.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# myProcedure3.buildStep(lambda: execute(), passed, error1, error2, allOtherErrors)
# # myProcedure3.buildStep(execute, passed, error1, error2, allOtherErrors)
# # myProcedure3.buildStep(execute, passed, error1, error2, allOtherErrors)

# myProcedureManager = packet.ProcedureManager()
# myProcedureManager.addProcedure("1", myProcedure1)
# myProcedureManager.addProcedure("2", myProcedure2)
# myProcedureManager.addProcedure("3", myProcedure3)

# nameOfProcedureToRun = "2"

# myProcedureManager.startProcedure(nameOfProcedureToRun)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)
# myProcedureManager.validate(nameOfProcedureToRun, validate)

setupProcedure = procedures.Procedure()
setupProcedure.buildStep(lambda: packet.sendConnectPacket(controlSock, 1, dataPortNumber), validate, passed, error1, error2, allOtherErrors)
setupProcedure.buildStep(lambda: packet.sendAcknowledgePacket(controlSock, 1, 1), validate, passed, error1, error2, allOtherErrors)

getProcedure = procedures.Procedure()
getProcedure.buildStep(lambda: packet.sendGetPacket(controlSock, 1),
                        lambda: lastPacketIsAck(lastReviecedPacket),
                        passed, error1, error2, allOtherErrors)
getProcedure.buildStep(lambda: packet.sendAcknowledgePacket(controlSock, 1, 1), validate, passed, error1, error2, allOtherErrors)

putProcedure = procedures.Procedure()
putProcedure.buildStep(lambda: packet.sendPutPacket(controlSock, 1),
                        lambda: lastPacketIsAck(lastReviecedPacket),
                        passed, error1, error2, allOtherErrors)
putProcedure.buildStep(lambda: packet.sendAcknowledgePacket(controlSock, 1, 1), validate, passed, error1, error2, allOtherErrors)

deleteProcedure = procedures.Procedure()
deleteProcedure.buildStep(lambda: packet.sendDeletePacket(controlSock, 1),
                        lambda: lastPacketIsAck(lastReviecedPacket),
                        passed, error1, error2, allOtherErrors)
deleteProcedure.buildStep(lambda: packet.sendAcknowledgePacket(controlSock, 1, 1), validate, passed, error1, error2, allOtherErrors)

listProcedure = procedures.Procedure()
listProcedure.buildStep(lambda: packet.sendListRequestPacket(controlSock, 1),
                        lambda: lastPacketIsAck(lastReviecedPacket),
                        passed, error1, error2, allOtherErrors)
listProcedure.buildStep(lambda: packet.sendAcknowledgePacket(controlSock, 1, 1), validate, passed, error1, error2, allOtherErrors)

disconnectProcedure = procedures.Procedure()
disconnectProcedure.buildStep(lambda: packet.sendDisconnectPacket(controlSock, 1), validate, passed, error1, error2, allOtherErrors)

procedureManager = procedures.ProcedureManager()
procedureManager.addProcedure("Setup", setupProcedure)
procedureManager.addProcedure("Get", getProcedure)
procedureManager.addProcedure("Put", putProcedure)
procedureManager.addProcedure("Delete", deleteProcedure)
procedureManager.addProcedure("List", listProcedure)
procedureManager.addProcedure("Quit", disconnectProcedure)

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

# Creates a control and data socket
controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lastReviecedPacket = packet.Packet()

# Connect control sock to the server
controlSock.connect((serverMachineAddress, serverControlPortNumber))

# packet.sendConnectPacket(controlSock, 1, dataPortNumber)
# lastReviecedPacket = packet.recvPacket(controlSock)
# if lastReviecedPacket.command == "ConAck":
#     response_to_ConnectAcknowledmentPacket(lastReviecedPacket.number, lastReviecedPacket.data)

print("Connecting to the server")

procedureManager.startProcedure("Setup")
lastReviecedPacket = packet.recvPacket(controlSock)
procedureManager.validateActiveProcedure()
# procedureManager.validateActiveProcedure()






while True:

    print ("ftp>", end =" ")

    inputRaw = input()

    inputArgs = list(map(str, inputRaw.split(' ')))

    if inputArgs[0] in ftpCommands:
        ftpCommands[inputArgs[0]](inputArgs)
    else:
        errorFTPCommand(inputArgs)
    
    lastReviecedPacket = packet.recvPacket(controlSock)
    if(procedureManager.anyProcedureIsRunning()):
        procedureManager.validateActiveProcedure()

