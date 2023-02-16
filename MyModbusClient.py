From scapy.all import *
from Modbus import *
import time

# Defining the script variables
srcIP = '192.168.1.1'
srcPort = random.randit(1024, 65535)
dstIP = '192.168.1.2'
dstPort = 502
seqNr = random.randit(444, 8765432)
ackNr = 0
transID = random.randit(44, 44444)

def updateSeqAndAckNrs(sendPkt, recdPkt):
    # Keep track of tcp sequence and acknowledge numbers
    global seqNr
    global ackNr


def main():
    print("MyModbusClient")

if __name__ == '__main__':
	main()
