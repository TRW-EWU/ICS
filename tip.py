#!/usr/bin/env/python3

import argparse
import socket
import sys

from MyModbusServer import MyModbusServer
from MyModbusClient import MyModbusClient

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--server", dest="server", help="SERVER: modbus, profinet, s7")
	parser.add_argument("-c", "--client", dest="client", help="CLIENT: modbus, profinet, s7")
	arguments = parser.parse_args()
	# if not arguments.aaa:
		# parser.error("[-] Please specify arg 'aaa' .")
	return arguments

def hack():
	print("Hack...")

	hostName = socket.gethostname()
	print("HostName: " + hostName)

	ip_addr = socket.gethostbyname(hostName)
	print("My IP address is: " + ip_addr)

	import os
	#q = os.system('ifconfig')
	#print(q)

	import platform
	#print(platform.node())

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# connect() for UDP doesn't send packets
	#s.connect(('10.0.0.0', 0)) 
	s.connect(('192.0.0.0', 0)) 
	print(s.getsockname()[0])

################### Main #######################

def main():
	options = get_arguments()

	if (options.server != None):
		if (options.server == 'modbus'):
			svr = MyModbusServer()
			svr.modbus_server()

	if (options.client != None):
		if (options.client == 'modbus'):
			client = MyModbusClient()
			client.modbus_client()

if __name__ == '__main__':
	print(sys.version)
	main()
	#hack()


