from scapy.all import *
from Modbus import *

import ipaddress
import os
import netifaces
import re
import subprocess
import time

# # Defining the script variables
srcIP = '10.0.0.195'

srcPort = random.randint(1024, 65535)
dstIP = '10.101.68.73'
dstIP = '10.0.0.142'
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
        #print("BEGIN: MyModbusClient...")

        self.hostName = socket.gethostname()

        # REVISIT: Will this work on Private IP with no internet access?
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.srcIP = s.getsockname()[0]

        # Get the subnet mask
        gws = netifaces.gateways()
        default_interface = gws['default'][netifaces.AF_INET][1]
        self.subnetMask = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['netmask']

        # Get the gateway
        self.gateway = "1.1.1.1 ???"

        # Get the MAC address
        #ifconfig_result = subprocess.check_output(["ifconfig", "eth0"])
        ifconfig_result = subprocess.check_output(["ifconfig"])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
        self.macAddress = mac_address_search_result.group(0)

        # Get the network interface
        self.ipInterface = ipaddress.IPv4Interface(self.srcIP + '/' + self.subnetMask)

        #print("END: ...MyModbusClient\n")

    def run(self):
        #print("Modbus Client ....")
        self.displayModbusMenu()

    def getNetInfo(self):
        print(f"Hostname: {self.hostName}")
        print(f"Local IP: {self.srcIP}")
        print(f"Subnet Mask: {self.subnetMask}")
        print(f"Gateway: {self.gateway}")
        print(f"MAC Address: {self.macAddress}")
        print(f"IP Interface: {self.ipInterface.network}")

    def displayModbusMenu(self):
        flagLoop = True
        os.system('clear')
        while flagLoop:
            print("\n\n\tModbus Client Menu")
            print("\t******************\n")
            print("\t  1. Get Network Information")
            print("\t  2. two")
            print("\t  3. three")
            print("\t  4. four")
            print("\t  5. five")
            print("\t  6. Quit\n")
            iChoice = input("\tEnter Selection: ")
            print("\n")

            if iChoice == '1':
                self.getNetInfo()
            elif iChoice == '2':
                print("two")
            elif iChoice == '3':
                print("three")
            elif iChoice == '4':
                print("four")
            elif iChoice == '5':
                print("five")
            elif iChoice == '6':
                print("six")
                flagLoop = False
            else:
                print("Invalid Choice")



