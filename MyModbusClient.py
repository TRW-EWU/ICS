from scapy.all import *
from Modbus import *
import time

# # Defining the script variables
srcIP = '10.101.68.80'
srcPort = random.randint(1024, 65535)
dstIP = '192.168.1.2'
dstPort = 502
seqNr = random.randint(444, 8765432)
ackNr = 0
transID = random.randint(44, 44444)

def updateSeqAndAckNrs(sendPkt, recdPkt):
    # Keep track of tcp sequence and acknowledge numbers
    global seqNr
    global ackNr
    seqNr = seqNr + len(sendPkt[TCP].payload)
    ackNr = ackNr + len(recvdPkt[TCP].payload)

def tcpHandshake():
    # Establish a connection with the server by means of the tcp
    # three-way handshake
    # Note: linux might send an RST for forged SYN packets. Disabe it by executing:
    # > iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <src_ip> -j DROP
    global seqNr
    global ackNr

    # Create SYN packet
    ip = IP(src=srcIP, dst=dstIP)
    print(ip)
    print(ip.show())
    SYN = TCP(sport=srcPort, dport=dstPort, flags='S', seq=seqNr, ack=ackNr)
    print(SYN)
    print(SYN.show())
    pktSYN = ip/SYN
    print(pktSYN)
    print(pktSYN.show())

    # send SYN packet and receive SYN/ACK packet
    print("TRW QAZ TRW...")
    pktSYNACK = sr1(pktSYN)
    #print(pktSYNACK.show())
    print("TRW QAZ TRW")

def ThomTest():
    print("ThomTest")
    # First establish a connection. The packet returned by the
    # function contains the connection parameters
    ConnectionPkt = tcpHandshake()


class MyModbusClient:
    def __init__(self):
        self.x = 4

    def modbus_client(self):
        print("Modbus Client ....")
        ThomTest()



