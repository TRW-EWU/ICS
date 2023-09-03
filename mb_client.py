from scapy.all import *
from Modbus.Modbus import *
import time

# # Defining the script variables
srcIP = '10.0.0.233'
srcPort = random.randint(1024, 65535)

dstIP = '10.0.0.73'
dstPort = 502

seqNr = random.randint(444, 8765432)
ackNr = 0

transID = random.randint(44, 44444)

def tcpHandshake():
    #print("BEGIN: tcpHandshake...")
    # Establish a connection with the server by means of the tcp
    # three-way handshake
    # Note: linux might send an RST for forged SYN packets. Disabe it by executing:
    #
    # sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <src_ip> -j DROP
    #
    global seqNr
    global ackNr

    # Create SYN packet
    ip = IP(src=srcIP, dst=dstIP)
    #print(ip.show())
    
    SYN = TCP(sport=srcPort, dport=dstPort, flags='S', seq=seqNr, ack=ackNr)
    #print(SYN.show())

    pktSYN = ip/SYN
    #print(pktSYN.show())

    # Send the SYN packet and receive SYN/ACK packet
    pktSYNACK = sr1(pktSYN)
    # print(pktSYNACK.show())

    # Create the ACK packet
    ackNr = pktSYNACK.seq + 1
    seqNr = seqNr + 1

    pktACK = TCP(sport=srcPort, dport=dstPort, flags='A', seq=seqNr, ack=ackNr)
    send(ip/pktACK)
    
    #print("END: ...tcpHandshake\n")
    return ip/pktACK

def updateSeqAndAckNrs(sendPkt, recvdPkt):
    #print("BEGIN: updateSeqAndAckNrs...")
    # Keep track of tcp sequence and acknowledge numbers
    global seqNr
    global ackNr
    seqNr = seqNr + len(sendPkt[TCP].payload)
    ackNr = ackNr + len(recvdPkt[TCP].payload)
    #print("END: ...updateSeqAndAckNrs\n")

def sendAck():
    #print("BEGIN: sendAck...")
    # Create the acknowledge packet
    ip = IP(src=srcIP, dst=dstIP)
    ACK = TCP(sport=srcPort, dport=dstPort, flags='A', seq=seqNr, ack=ackNr)

    pktACK = ip/ACK

    # Send the acknowledge packet
    send(pktACK)
    #print("END: ...sendAck\n")




def endConnection():
    #print("BEGIN: endConnection...")
    # Create the RST packet
    ip = IP(src=srcIP, dst=dstIP)
    RST = TCP(sport=srcPort, dport=dstPort, flags='RA', seq=seqNr, ack=ackNr)

    pktRST = ip/RST

    # Send the RST packet
    send(pktRST)
    #print("END: ...endConnection\n")

def connectedSend(pkt):
    #print("BEGIN: ConnectedSend...")
    # Update packet's sequence and acknowledge numbers
    # before sending
    pkt[TCP].flags = 'PA'
    pkt[TCP].seq = seqNr
    pkt[TCP].ack = ackNr
    send(pkt)
    #print("END: ...ConnectedSend\n")


def ThomTest():
    #print("BEGIN: ThomTest...")
    # First establish a connection. The packet returned by the
    # function contains the connection parameters
    #print("DEBUG: Received ACK from Modbus Server...")
    ConnectionPkt = tcpHandshake()
    #print(ConnectionPkt.show())

    # With the connection packet as a base, create a Modbus
    # reques packet to read coils
    ModbusPkt = ConnectionPkt/ModbusADU()/ModbusPDU01_Read_Coils()
    #print("DEBUG: Modbus packet to send...")
    #print(ModbusPkt.show())

    # Set the function code, start and stop registers and define
    # the Unit ID
    ModbusPkt[ModbusADU].unitId = 1
    
    ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 2 
    
    ModbusPkt[ModbusPDU01_Read_Coils].quantity = 6 

    # Create a unique transaction ID
    ModbusPkt[ModbusADU].transID = transID + 3
    ModbusPkt[ModbusPDU01_Read_Coils].startAddr = 0
    #print("DEBUG: Modbus packet with PDU info to send...")
    #print(ModbusPkt.show())

    # send the packet
    connectedSend(ModbusPkt)
    # Wait for response packets and filter out the Modbus response packet
    Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push|tcp-ack) != 0')
    #print("DEBUG: Results...")
    #print(Results.show())

    #print("DEBUG: Response Packet...")
    ResponsePkt = Results[0]
    ResponsePkt.show()
    #print("DEBUG: ...Response Packet\n")

    updateSeqAndAckNrs(ModbusPkt, ResponsePkt)

    sendAck()
    endConnection()
    #print("END: ...ThomTest\n")


class MyModbusClient:
    def __init__(self):
        self.x = 4

    def modbus_client(self):
        #print("Modbus Client ....")
        ThomTest()

#print("TRW: mb_client")
ConnectionPkt = tcpHandshake()

ModbusPkt = ConnectionPkt/ModbusADU()/ModbusPDU01_Read_Coils()

###############################
# Read Holding Register FC = 01

ModbusPkt[ModbusADU].transID = transID + 3
ModbusPkt[ModbusADU].unitId = 1

ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 1 
ModbusPkt[ModbusPDU01_Read_Coils].startAddr = 0
ModbusPkt[ModbusPDU01_Read_Coils].quantity = 6 

connectedSend(ModbusPkt)

Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push | tcp-ack) != 0')
ResponsePkt = Results[0]
# ResponsePkt.show()

updateSeqAndAckNrs(ModbusPkt, ResponsePkt)
sendAck()

###########################
# Read Input Status FC = 02

ModbusPkt[ModbusADU].transID = transID + 3 + 3
ModbusPkt[ModbusADU].unitId = 1

ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 2 
ModbusPkt[ModbusPDU01_Read_Coils].startAddr = 0
ModbusPkt[ModbusPDU01_Read_Coils].quantity = 6 

connectedSend(ModbusPkt)

Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push | tcp-ack) != 0')
ResponsePkt = Results[0]
# ResponsePkt.show()

updateSeqAndAckNrs(ModbusPkt, ResponsePkt)
sendAck()

###############################
# Read Holding Register FC = 03

ModbusPkt[ModbusADU].transID = transID + 3 + 3 + 3
ModbusPkt[ModbusADU].unitId = 1

ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 3 
ModbusPkt[ModbusPDU01_Read_Coils].startAddr = 0
ModbusPkt[ModbusPDU01_Read_Coils].quantity = 1 

connectedSend(ModbusPkt)

Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push | tcp-ack) != 0')
ResponsePkt = Results[0]
# ResponsePkt.show()

updateSeqAndAckNrs(ModbusPkt, ResponsePkt)
sendAck()

##############################
# Read Input Registers FC = 04

ModbusPkt[ModbusADU].transID = transID + 3 + 3 + 3 + 3
ModbusPkt[ModbusADU].unitId = 1

ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 4 
ModbusPkt[ModbusPDU01_Read_Coils].startAddr = 0
ModbusPkt[ModbusPDU01_Read_Coils].quantity = 4 

connectedSend(ModbusPkt)

Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push | tcp-ack) != 0')
ResponsePkt = Results[0]
# ResponsePkt.show()

updateSeqAndAckNrs(ModbusPkt, ResponsePkt)
sendAck()

##############################
# Write Single Coil FC = 05

ModbusPkt = ConnectionPkt/ModbusADU()/ModbusPDU05_Write_Single_Coil()

ModbusPkt[ModbusADU].transID = transID + 3 + 3 + 3 + 3 + 3
ModbusPkt[ModbusADU].unitId = 1

ModbusPkt[ModbusPDU05_Write_Single_Coil].funcCode = 5 
ModbusPkt[ModbusPDU05_Write_Single_Coil].outputAddr = 0
#ModbusPkt[ModbusPDU05_Write_Single_Coil].outputValue = 0xFF00 
ModbusPkt[ModbusPDU05_Write_Single_Coil].outputValue = 0x0000 

connectedSend(ModbusPkt)

Results = sniff(count=1, filter='tcp[tcpflags] & (tcp-push | tcp-ack) != 0')
ResponsePkt = Results[0]
# ResponsePkt.show()

updateSeqAndAckNrs(ModbusPkt, ResponsePkt)
sendAck()

###############################

endConnection()
