# The server

# Needs to start up with
# pythonserv.py <PORTNUMBER> and then accepts requests at that port

# Valid commands
# pythonserv.py <PORTNUMBER>
# pythonserv.py help

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

def openControlSock():
    global clientControlSock
    global controlSock
    global allProcedures
    
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    controlSock.bind((get_ip(), controlPortNumber))

    # Start listening on the socket
    controlSock.listen()

    allProcedures["Setup"] = ([("000Ack", clientControlSock)],[response_to_AcknowledgePacket])


    sockName = controlSock.getsockname()

    print ("Waiting for connections on control channel...")
    print (sockName)


    # Accept connections
    clientControlSock, addr = controlSock.accept()

    print ("Accepted connection from client on control channel: ", addr)
    print ("\n")

def openDataSock():
    global clientDataSock
    global dataSock

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dataSock.bind((get_ip(), dataPortNumber))

    dataSock.listen()

    sockName = dataSock.getsockname()

    print ("Waiting for connections on data channel...")
    print (sockName)

    clientDataSock, addr = dataSock.accept()

    print ("Accepted connection from client on data channel: ", addr)
    print ("\n")

    # lastPacket = packet.recvPacket(clientDataSock)

def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        print("unexpected exception when checking if a socket is closed")
        print("", e)
        return False
    return False

def response_to_ConnectPacket(recieved: packet.Packet):
    global clientDataPortNumber
    
    clientDataPortNumber = clientDataPortNumber.from_bytes(recieved.data)

    print ("recieved a connection packet")
    print ("", recieved.data)
    print ("client data port number is ", clientDataPortNumber)

    packet.sendConnectAcknowledgmentPacket(clientControlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(recieved: packet.Packet):
    

    global clientDataPortNumber
    
    clientDataPortNumber = clientDataPortNumber.from_bytes(recieved.data)

    print ("recieved a connection acknowledgement packet")
    print ("", recieved.data)
    print ("client data port number is ", clientDataPortNumber)

    packet.sendAcknowledgePacket(clientControlSock, 1, recieved.number)

def response_to_DisconnectPacket(recieved: packet.Packet):
    print ("closing")

    # Close our side
    clientControlSock.close()
    controlSock.close()
    quit()

def response_to_GetPacket(recieved: packet.Packet):
    print ("recieved a get packet")

    global runningProcedure
    global clientDataSock
    global sendingFileName
    global transferFileData

    sendingFileName = recieved.data.decode()

    if os.path.isfile(sendingFileName):

        runningProcedure = "Get"

        print("Found the file")
        fileObj = open(sendingFileName, "rb")
        transferFileData = fileObj.read()
        print(transferFileData)

        packet.sendAcknowledgePacket(clientControlSock, 1, recieved.number)
        openDataSock()
        allProcedures["Get"] = ([("000Con", clientDataSock),("000Ack", clientDataSock),("000Ack", clientDataSock)],[sendConAck_On_DataChannel,sendFMan,sendFile])

    else:
        print("That file does not exist")
        packet.sendInvalidPacket(clientControlSock, 1)
        return

def response_to_PutPacket(recieved: packet.Packet):
    global clientDataSock
    global runningProcedure
    global recievingFileName

    recievingFileName = recieved.data.decode()

    print ("recieved a put packet for the file: ", recievingFileName)

    runningProcedure = "Put"
    

    packet.sendAcknowledgePacket(clientControlSock, 1, recieved.number)
    openDataSock()

    allProcedures["Put"] = ([("000Con", clientDataSock),("00FMan", clientDataSock),("00File", clientDataSock)],[sendConAck_On_DataChannel,sendAck_On_DataChannel,response_to_FilePacket])

def response_to_DeletePacket(recieved: packet.Packet):
    global runningProcedure
    global recievingFileName
    
    recievingFileName = recieved.data.decode()

    print ("recieved a delete packet for the file: ", recievingFileName)

    

    if os.path.isfile(recievingFileName):
        deleteFile(recievingFileName)
        packet.sendAcknowledgePacket(clientControlSock, 1, 1)
    else:
        print("That file does not exist")
        packet.sendInvalidPacket(clientControlSock, 1)

    # packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_ListRequestPacket(recieved: packet.Packet):
    global runningProcedure
    global clientDataSock
    global sendingFileName
    global transferFileData
    
    print ("recieved a list request packet")

    runningProcedure = "List"

    # fileObj = open(sendingFileName, "rb")
    # transferFileData = fileObj.read()
    # print(transferFileData)

    transferFileData_as_str = ""

    listdir = os.listdir()

    for item in listdir:
        transferFileData_as_str = transferFileData_as_str + "\n" + item

    transferFileData = transferFileData_as_str.encode()

    packet.sendAcknowledgePacket(clientControlSock, 1, recieved.number)
    openDataSock()
    allProcedures["List"] = (
        [
        ("000Con", clientDataSock),
        ("000Ack", clientDataSock),
        ("000Ack", clientDataSock)],
        [
        sendConAck_On_DataChannel,
        sendFMan,
        sendFile])


def response_to_AcknowledgePacket(recieved: packet.Packet):
    print ("recieved a acknowledge packet")

def response_to_InvalidPacket(recieved: packet.Packet):
    print ("recieved a invalid packet")

def response_to_FileManifestPacket(recieved: packet.Packet):
    print ("recieved a file manifest packet")

def response_to_FilePacket(recieved: packet.Packet):
    print ("recieved a file packet")

    if os.path.isfile(recievingFileName):
        fileObject = open(recievingFileName, "w+b")
    else:
        fileObject = open(recievingFileName, "xb")
    
    fileObject.write(recieved.data)
    fileObject.close()

    closeDataChannel(recieved)


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

def sendFMan(recieved: packet.Packet):
    packet.sendFileManifestPacket(clientDataSock, 1)

def sendFile(recieved: packet.Packet):
    packet.sendFilePacket(clientDataSock, 1, transferFileData)
    closeDataChannel(recieved)

def sendAck(recived: packet.Packet):
    packet.sendAcknowledgePacket(clientControlSock, 1, 1)

def sendAck_On_DataChannel(recived: packet.Packet):
    packet.sendAcknowledgePacket(clientDataSock, 1, 1)

def closeDataChannel(recieved: packet.Packet):
    global clientDataSock
    global dataSock

    packet.sendAcknowledgePacket(clientDataSock, 1, 1)
    # clientDataSock.detach()
    dataSock.close()
    

def sendConAck_On_DataChannel(recieved: packet.Packet):
    packet.sendConnectAcknowledgmentPacket(clientDataSock, 1, dataPortNumber)
    pass


def deleteFile(fileName):
    if os.path.isfile(fileName):
        os.remove(fileName)

def validateCommandLineArgs():
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


def serverSetup():
    validateCommandLineArgs()

    # Global variables
    global controlPortNumber
    global dataPortNumber
    global clientDataPortNumber

    global controlSock
    global dataSock
    global clientControlSock
    global clientDataSock

    global isExpectingPacket
    global expectedPacketName
    global runningProcedure
    global procedureStep
    global allProcedures

    # Sets the main control port to list to
    controlPortNumber = int(sys.argv[1])

    # Sets the port number that data will be recieved on
    dataPortNumber = 1235

    clientDataPortNumber = 0

    # Create a welcome socket. 
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientControlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientDataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Procedures
    isExpectingPacket = False
    expectedPacketName = ""

    runningProcedure = ""
    procedureStep = 0

    allProcedures = {
        # "Setup" : ([("000Ack", clientControlSock)],[response_to_AcknowledgePacket])
    }


    openControlSock()

    
def coreLoop():
    global runningProcedure
    global procedureStep
    global allProcedures
    global lastPacket

    while True:

        if(runningProcedure != ""):
            # a procedure is running

            procedureExpectedReplies, procedureResponses = allProcedures[runningProcedure]

            if procedureStep < len(procedureExpectedReplies):

                name, sock = procedureExpectedReplies[procedureStep]

                # if is_socket_closed(sock):
                #     print("Expected packet from a closed socket")
                #     quit()
                # else:

                lastPacket = packet.recvPacket(sock)

                if(packet.isExpectedPacket(lastPacket, name)):
                    procedureResponses[procedureStep](lastPacket)
                    procedureStep += 1
                else:
                    print("recieved unexpected packet")
                    
            else:
                runningProcedure = ""
                procedureStep = 0
        else:
            # No procedures are running listen for new procedures

            lastPacket = packet.recvPacket(clientControlSock)
            respondToPacket(lastPacket)

def main():
    serverSetup()
    coreLoop()

if __name__=="__main__":
    main()