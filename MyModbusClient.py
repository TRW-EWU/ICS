from scapy.all import *
from Modbus import *
import time

# # Defining the script variables
srcIP = '10.0.0.142'
srcPort = random.randint(1024, 65535)
dstIP = '10.0.0.195'
dstPort = 502
seqNr = random.randint(444, 8765432)
ackNr = 0
transID = random.randint(44, 44444)

def updateSeqAndAckNrs(sendPkt, recvdPkt):
    print("BEGIN: updateSeqAndAckNrs...")
    # Keep track of tcp sequence and acknowledge numbers
    global seqNr
    global ackNr
    seqNr = seqNr + len(sendPkt[TCP].payload)
    ackNr = ackNr + len(recvdPkt[TCP].payload)
    print("END: ...updateSeqAndAckNrs\n")

def sendAck():
    print("BEGIN: sendAck...")
    # Create the acknowledge packet
    ip = IP(src=srcIP, dst=dstIP)
    ACK = TCP(sport=srcPort, dport=dstPort, flags='A', seq=seqNr, ack=ackNr)

    pktACK = ip/ACK

    # Send the acknowledge packet
    send(pktACK)
    print("END: ...sendAck\n")


def tcpHandshake():
    print("BEGIN: tcpHandshake...")
    # Establish a connection with the server by means of the tcp
    # three-way handshake
    # Note: linux might send an RST for forged SYN packets. Disabe it by executing:
    # > iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <src_ip> -j DROP
    global seqNr
    global ackNr

    # Create SYN packet
    ip = IP(src=srcIP, dst=dstIP)
    #print(ip)
    #print(ip.show())
    SYN = TCP(sport=srcPort, dport=dstPort, flags='S', seq=seqNr, ack=ackNr)
    #print(SYN)
    #print(SYN.show())
    pktSYN = ip/SYN
    #print(pktSYN)
    #print(pktSYN.show())

    # send SYN packet and receive SYN/ACK packet
    #print("TRW QAZ TRW...")
    pktSYNACK = sr1(pktSYN)
    #print(pktSYNACK.show())
    #print("TRW QAZ TRW")

    # Create the ACK packet
    ackNr = pktSYNACK.seq + 1
    seqNr = seqNr + 1
    ACK = TCP(sport=srcPort, dport=dstPort, flags='A', seq=seqNr, ack=ackNr)
    #print("DEBUG: Sending ACK to Modbus Server...")
    send(ip/ACK)
    
    print("END: ...tcpHandshake\n")
    return ip/ACK

def endConnection():
    print("BEGIN: endConnection...")
    # Create the RST packet
    ip = IP(src=srcIP, dst=dstIP)
    RST = TCP(sport=srcPort, dport=dstPort, flags='RA', seq=seqNr, ack=ackNr)

    pktRST = ip/RST

    # Send the RST packet
    send(pktRST)
    print("END: ...endConnection\n")

def connectedSend(pkt):
    print("BEGIN: ConnectedSend...")
    # Update packet's sequence and acknowledge numbers
    # before sending
    pkt[TCP].flags = 'PA'
    pkt[TCP].seq = seqNr
    pkt[TCP].ack = ackNr
    send(pkt)
    print("END: ...ConnectedSend\n")


def ThomTest():
    print("BEGIN: ThomTest...")
    # First establish a connection. The packet returned by the
    # function contains the connection parameters
    ConnectionPkt = tcpHandshake()
    #print("DEBUG: Received ACK from Modbus Server...")
    #print(ConnectionPkt.show())

    # With the connection packet as a base, create a Modbus
    # reques packet to read coils
    ModbusPkt = ConnectionPkt/ModbusADU()/ModbusPDU01_Read_Coils()
    #print("DEBUG: Modbus packet to send...")
    #print(ModbusPkt.show())

    # Set the function code, start and stop registers and define
    # the Unit ID
    ModbusPkt[ModbusADU].unitId = 1
    
    ModbusPkt[ModbusPDU01_Read_Coils].funcCode = 4
    
    ModbusPkt[ModbusPDU01_Read_Coils].quantity = 10

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

    print("DEBUG: Response Packet...")
    ResponsePkt = Results[0]
    ResponsePkt.show()
    print("DEBUG: ...Response Packet\n")

    updateSeqAndAckNrs(ModbusPkt, ResponsePkt)

    sendAck()
    endConnection()
    print("END: ...ThomTest\n")




class MyModbusClient:
    def __init__(self):
        self.x = 4

    def modbus_client(self):
        print("Modbus Client ....")
        ThomTest()



