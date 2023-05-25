#!/usr/bin/env/python3

import argparse
import socket
import sys

from MyModbusServer import MyModbusServer
from MyModbusClient import MyModbusClient

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", "--modbus", dest="modbus", help="client, server")
	parser.add_argument("-f", "--function", dest="function", help="scan, test, map, define")
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


def myScan():
	print("My Scanner")

def myTest():
	print("My Test")

def myMap():
	print("My Map")

def myDefine():
	print("My Define")

################### Main #######################

def main():
	options = get_arguments()
	print(options)

	if (options.modbus != None):
		if (options.modbus == 'server'):
			svr = MyModbusServer()
			svr.modbus_server()
		elif (options.modbus == 'client'):
			client = MyModbusClient()
			client.modbus_client()
	elif (options.function != None):
		if (options.function == 'scan'):
			myScan()
		elif (options.function == 'test'):
			myTest()
		elif (options.function == 'map'):
			myMap()
		elif (options.function == 'define'):
			myDefine()

if __name__ == '__main__':
	print(sys.version)
	main()
	#hack()


