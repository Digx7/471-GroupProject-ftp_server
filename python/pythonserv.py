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

def openControlSock():
    global clientControlSock
    
    # Bind the socket to the port
    controlSock.bind((get_ip(), controlPortNumber))

    # Start listening on the socket
    controlSock.listen()

    sockName = controlSock.getsockname()

    print ("Waiting for connections...")
    print (sockName)


    # Accept connections
    clientControlSock, addr = controlSock.accept()

    print ("Accepted connection from client: ", addr)
    print ("\n")


def response_to_ConnectPacket(recieved: packet.Packet):
    print ("recieved a connection packet")

    clientDataPortNumber.from_bytes(recieved.data)

    packet.sendConnectAcknowledgmentPacket(clientControlSock, 1, dataPortNumber)

def response_to_ConnectAcknowledmentPacket(recieved: packet.Packet):
    print ("recieved a connection acknowledgement packet")

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_DisconnectPacket(recieved: packet.Packet):
    print ("closing")

    # Close our side
    clientControlSock.close()
    controlSock.close()
    quit()

def response_to_GetPacket(recieved: packet.Packet):
    print ("recieved a get packet")

    # TODO: check if file exists
    # If file exists open Data sock

    # dataSock.bind((get_ip(), dataPortNumber))

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    global runningProcedure
    runningProcedure = "Get"

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_PutPacket(recieved: packet.Packet):
    print ("recieved a put packet")

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_DeletePacket(recieved: packet.Packet):
    print ("recieved a delete packet")

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_ListRequestPacket(recieved: packet.Packet):
    print ("recieved a list request packet")

    packetNumber = 0
    packetNumber.from_bytes(recieved.data)

    packet.sendAcknowledgePacket(clientControlSock, 1, packetNumber)

def response_to_AcknowledgePacket(recieved: packet.Packet):
    print ("recieved a acknowledge packet")

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



def sendAck(reived: packet.Packet):
    packet.sendAcknowledgePacket(clientControlSock, 1, 1)

allProcedures = {
    "Setup" : (["000Ack"],[response_to_AcknowledgePacket]),
    "Get" : (["00FMan", "000Get"],[sendAck, sendAck])
}



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
    global isExpectingPacket
    global expectedPacketName
    global runningProcedure
    global procedureStep

    # Sets the main control port to list to
    controlPortNumber = int(sys.argv[1])

    # Sets the port number that data will be recieved on
    dataPortNumber = 300

    clientDataPortNumber = 0

    # Create a welcome socket. 
    controlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Procedures
    isExpectingPacket = False
    expectedPacketName = ""

    runningProcedure = ""
    procedureStep = 0

    openControlSock()

    
def coreLoop():
    global runningProcedure
    global procedureStep
    global allProcedures

    while True:

        if(runningProcedure != ""):
            # a procedure is running

            procedureExpectedPackets, procedureResponses = allProcedures[runningProcedure]

            if procedureStep < len(procedureExpectedPackets):
                lastPacket = packet.recvPacket(clientControlSock)
                if(packet.isExpectedPacket(lastPacket, procedureExpectedPackets[procedureStep])):
                    procedureResponses[procedureStep](lastPacket)
                    procedureStep += 1
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