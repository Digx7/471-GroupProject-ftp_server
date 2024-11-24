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
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import application.PacketLib.packet as packet

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip



# All the ftp commands availble once the connection is set

def connectToServer():
    print("ACTION: Connecting to the server control channel")
    global controlSock
    global allProcedures

    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    controlSock.connect((serverMachineAddress, serverControlPortNumber))
    
    # allProcedures["SetUp"] = (
    #     [("ConAck", controlSock)],
    #     [response_to_ConnectAcknowledmentPacket])
    # allProcedures["Get"] = ([("000Ack", controlSock),("ConAck", dataSock),("000Ack", dataSock),("000Ack",dataSock)],[connectOnDataChannel, sendFMan, sendFilePacket, closeDataChannel])
    # allProcedures["Put"] = ([("000Ack", controlSock),("ConAck", dataSock),("000Ack", dataSock),("000Ack",dataSock)],[connectOnDataChannel, sendFMan, sendFilePacket, closeDataChannel])


    allProcedures["SetUp"] = [
        (
            controlSock,
            [("ConAck", response_to_ConnectAcknowledmentPacket, False)]
        )
    ]


    allProcedures["Get"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_FilePacket, False)]
        )
    ]

    allProcedures["Put"] = [
        (
            controlSock,
            [("000Ack", connectOnDataChannel, False)]
        ),
        (
            dataSock,
            [("ConAck", sendFMan, False)]
        ),
        (
            dataSock,
            [("000Ack", sendFilePacket, False)]
        ),
        (
            dataSock,
            [("000Ack", closeDataChannel, False)]
        )
    ]

    allProcedures["Delete"] = [
        (
            controlSock,
            [
            ("000Ack", response_to_AcknowledgePacket, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        )
    ]

    allProcedures["List"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_ListFilePacket, False)]
        )
    ]


    expectPacket("ConAck")
    global runningProcedure
    runningProcedure = "SetUp"
    packet.sendConnectPacket(controlSock, 1, dataPortNumber)

def connectToServer_On_DataChannel():
    print("ACTION: Connecting to server data channel")
    global dataSock

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock.connect((serverMachineAddress, serverDataPortNumber))

    # allProcedures["Get"] = (
    #     [("000Ack", controlSock),
    #      ("ConAck", dataSock),
    #     #  Comment
    #      ("00FMan", dataSock),
    #      ("00File",dataSock)],
    #     [connectOnDataChannel, 
    #      sendAck_on_dataChannel, 
    #      sendAck_on_dataChannel, 
    #      response_to_FilePacket])
    
    # allProcedures["Put"] = (
    #     [("000Ack", controlSock),
    #     ("ConAck", dataSock),
    #     ("000Ack", dataSock),
    #     ("000Ack",dataSock)],
    #     [connectOnDataChannel, 
    #     sendFMan, 
    #     sendFilePacket, 
    #     closeDataChannel])


    allProcedures["Get"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_FilePacket, False)]
        )
    ]

    allProcedures["Put"] = [
        (
            controlSock,
            [("000Ack", connectOnDataChannel, False)]
        ),
        (
            dataSock,
            [("ConAck", sendFMan, False)]
        ),
        (
            dataSock,
            [("000Ack", sendFilePacket, False)]
        ),
        (
            dataSock,
            [("000Ack", closeDataChannel, False)]
        )
    ]

    allProcedures["Delete"] = [
        (
            controlSock,
            [
            ("000Ack", response_to_AcknowledgePacket, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        )
    ]

    allProcedures["List"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_ListFilePacket, False)]
        )
    ]

    # allProcedures["Name"] = [
    #     # Step 1
    #     [
    #         (("PacName", controlSock), response_to_AcknowledgePacket), 
    #         (("Error1", controlSock), response_to_AcknowledgePacket)
    #     ]]

    expectPacket("ConAck")
    # global runningProcedure
    # runningProcedure = "SetUp"
    packet.sendConnectPacket(dataSock, 1, dataPortNumber)

# Downloads a file
def getFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("ERROR: A file name is needed")
        return
    
    global recievingFileName
    recievingFileName = inputArgs[1]
    # print("Getting file: " + recievingFileName)

    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Get"
    packet.sendGetPacket(controlSock, 1, recievingFileName)

# Uploads a file
def putFTPCommand(inputArgs):
    global transferFileData

    if len(inputArgs) < 2:
        print("ERROR: A file name is needed")
        return
    fileName = inputArgs[1]

    if os.path.isfile(fileName):
        print("ACTION: The file exists")
        fileObj = open(fileName, "rb")
        transferFileData = fileObj.read()
        # print(transferFileData)
    else:
        print("ERROR: That file does not exist")
        return


    # print("Uploading file: " + fileName)

    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Put"
    packet.sendPutPacket(controlSock, 1, fileName)

# Deletes a file
def deleteFTPCommand(inputArgs):
    if len(inputArgs) < 2:
        print("ERROR: A file name is needed")
        return
    fileName = inputArgs[1]
    # print("Deleting file: " + fileName)
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "Delete"
    packet.sendDeletePacket(controlSock, 1, fileName)

# Lists out all valid commands
def helpFTPCommand(inputArgs):
    print("\nValid commands:")
    print("get <FILENAME>")
    print("put <FILENAME>")
    print("delete <FILENAME>")
    print("ls")
    print("help")
    print("quit")
    print("exit")

# Lists out all files on FTP server
def lsFTPCommand(inputArgs):
    # print("Listing file names")
    expectPacket("000Ack")
    global runningProcedure
    runningProcedure = "List"
    packet.sendListRequestPacket(controlSock, 1)

# Quits execution
def quitFTPCommand(inputArgs):
    packet.sendDisconnectPacket(controlSock, 1)
    print("ACTION: Shutting Down")
    print("Goodbye!")
    quit()

# Runs if the command is not recognized
def errorFTPCommand(inputArgs):
    print("ERROR: Invalid command")
    print("    Use the help command to see all valid commands")

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


def closeDataChannel(recieved: packet.Packet):
    global dataSock
    dataSock.close()

def response_to_generic(recieved: packet.Packet):
    print("RECIEVED: Generic packet = ", recieved.command)

def response_to_ConnectPacket(recieved: packet.Packet):

    global serverDataPortNumber

    serverDataPortNumber = serverDataPortNumber.from_bytes(recieved.data)

    print ("RECIEVED: Connection packet | server data port number = ", serverDataPortNumber)

    packet.sendConnectAcknowledgmentPacket(controlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(recieved: packet.Packet):

    global serverDataPortNumber

    serverDataPortNumber = serverDataPortNumber.from_bytes(recieved.data)

    print ("RECIEVED: Connection Acknowledgment packet | server data port number = ", serverDataPortNumber)

    notExpectingPacket()

    packet.sendAcknowledgePacket(controlSock, 1, recieved.number)

def response_to_DisconnectPacket(recieved: packet.Packet):
    print ("RECIEVED: Disconnection packet")

def response_to_GetPacket(recieved: packet.Packet):
    print ("RECIEVED: Get packet")

def response_to_PutPacket(recieved: packet.Packet):
    print ("RECIEVED: Put packet")

def response_to_DeletePacket(recieved: packet.Packet):
    print ("RECIEVED: Delete packet")

def response_to_ListRequestPacket(recieved: packet.Packet):
    print ("RECIEVED: List Request packet")

def response_to_AcknowledgePacket(recieved: packet.Packet):
    print ("RECIEVED: Acknowledgement packet")
    notExpectingPacket()

def response_to_InvalidPacket(recieved: packet.Packet):
    print ("RECIEVED: Invalid packet")

def response_to_FileManifestPacket(recieved: packet.Packet):
    print ("RECIEVED: File Manifest packet")

def response_to_FilePacket(recieved: packet.Packet):
    print ("RECIEVED: File packet")

    if os.path.isfile(recievingFileName):
        print ("ACTION: overwriting existing file: ", recievingFileName)
        fileObject = open(recievingFileName, "w+b")
    else:
        print ("ACTION: writing new file: ", recievingFileName)
        fileObject = open(recievingFileName, "xb")
    
    fileObject.write(recieved.data)
    fileObject.close()

    closeDataChannel(recieved)

def response_to_ListFilePacket(recieved: packet.Packet):
    
    listOfFiles = recieved.data.decode()
    print(listOfFiles)
    
    closeDataChannel(recieved)

def response_to_FileStatusPacket(recieved: packet.Packet):
    print ("RECIEVED: File status packet")

def response_to_UnrecognizedPacket(recieved: packet.Packet):
    print ("ERROR: RECIEVED: Unrecognized packet")

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

def fileDoesntExistOnServer(recieved: packet.Packet):
    print("ERROR: That file does not exist on the server")


def sendFMan(recived: packet.Packet):
    packet.sendFileManifestPacket(dataSock, 1)

def sendFilePacket(recived: packet.Packet):
    # global transferFileData

    # print(transferFileData)

    packet.sendFilePacket(dataSock, 1, transferFileData)

def sendGet(recived: packet.Packet):
    packet.sendGetPacket(controlSock, 1, "Name")

def connectOnDataChannel(recived: packet.Packet):
    connectToServer_On_DataChannel()

def sendAck_on_dataChannel(recieved: packet.Packet):
    packet.sendAcknowledgePacket(dataSock, 1, 1)


def buildControlSock():
    # Creates a control socket
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    controlSock.connect((serverMachineAddress, serverControlPortNumber))

def validateCommandLineArgs():
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


def clientSetup():
    validateCommandLineArgs()

    # Global variables
    global serverMachineAddress
    global serverControlPortNumber

    global dataPortNumber
    global serverDataPortNumber

    global controlSock
    global dataSock

    global isExpectingPacket
    global expectedPacketName
    global runningProcedure
    global procedureStep
    global allProcedures

    # Gets command line arguments
    serverMachineAddress = str(sys.argv[1])
    serverControlPortNumber = int(sys.argv[2])

    # Sets the port number that data will be recieved on
    dataPortNumber = 200
    serverDataPortNumber = 0

    # Creates a control and data sockets socket
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Procedures
    isExpectingPacket = False
    expectedPacketName = ""

    runningProcedure = ""
    procedureStep = 0

    # allProcedures = {
    #     "SetUp" : ([("ConAck", controlSock)],[response_to_ConnectAcknowledmentPacket]),
    #     "Get" : ([("000Ack", controlSock),("ConAck", dataSock),("000Ack", dataSock),("000Ack",dataSock)],[connectOnDataChannel, sendFMan, sendFilePacket, closeDataChannel]),
    #     "Put" : ([("000Ack", controlSock),("ConAck", dataSock),("000Ack", dataSock),("000Ack",dataSock)],[connectOnDataChannel, sendFMan, sendFilePacket, closeDataChannel])
    # }

    allProcedures = {}

    allProcedures["SetUp"] = [
        (
            controlSock,
            [("ConAck", response_to_ConnectAcknowledmentPacket, False)]
        )
    ]


    allProcedures["Get"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_FilePacket, False)]
        )
    ]

    allProcedures["Put"] = [
        (
            controlSock,
            [("000Ack", connectOnDataChannel, False)]
        ),
        (
            dataSock,
            [("ConAck", sendFMan, False)]
        ),
        (
            dataSock,
            [("000Ack", sendFilePacket, False)]
        ),
        (
            dataSock,
            [("000Ack", closeDataChannel, False)]
        )
    ]

    allProcedures["Delete"] = [
        (
            controlSock,
            [
            ("000Ack", response_to_AcknowledgePacket, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        )
    ]

    allProcedures["List"] = [
        (
            controlSock,
            [
            ("000Ack", connectOnDataChannel, False),
            ("InvPac", fileDoesntExistOnServer, True)
            ]
        ),
        (
            dataSock,
            [("ConAck", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00FMan", sendAck_on_dataChannel, False)]
        ),
        (
            dataSock,
            [("00File", response_to_ListFilePacket, False)]
        )
    ]

    connectToServer()

def coreLoop():
    global runningProcedure
    global procedureStep
    global allProcedures
    
    while True:

        if(runningProcedure != ""):
            # a procedure is running

            # procedureExpectedReplies, procedureResponses = allProcedures[runningProcedure]
            

            # if procedureStep < len(procedureExpectedReplies):
            #     lastPacket = packet.recvPacket(procedureExpectedReplies[procedureStep][1])
            #     if(packet.isExpectedPacket(lastPacket, procedureExpectedReplies[procedureStep][0])):
            #         procedureResponses[procedureStep](lastPacket)
            #         procedureStep += 1
            # else:
            #     runningProcedure = ""
            #     procedureStep = 0

            procedureSteps = allProcedures[runningProcedure]

            if procedureStep < len(procedureSteps):
                sock = procedureSteps[procedureStep][0]
                responses = procedureSteps[procedureStep][1]

                lastPacket = packet.recvPacket(sock)

                for response in responses:
                    name = response[0]
                    action = response[1]
                    isEarlyTerminator = response[2]

                    if(packet.isExpectedPacket(lastPacket, name)):
                        action(lastPacket)
                        if not isEarlyTerminator:
                            procedureStep += 1
                        else:
                            runningProcedure = ""
                            procedureStep = 0
                
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

def main():
    clientSetup()
    coreLoop()

if __name__=="__main__":
    main()
