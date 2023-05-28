#!/usr/bin/env/python3

import argparse
import ipaddress
import netifaces
import pymodbus
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
	print(f"Hostname: {socket.gethostname()}")
	# This returns 127.0.1.1????
	local_ip = socket.gethostbyname(socket.gethostname())
	print(f"Local IP: {local_ip}")
	local_ip = "10.0.0.195"

	# get sub net mask
	gws = netifaces.gateways()
	default_interface = gws['default'][netifaces.AF_INET][1]
	subnet_mask = netifaces.ifaddresses(default_interface)[netifaces.AF_INET][0]['netmask']
	print(f"Subnet Mask: {subnet_mask}\n")

	# get the network
	ip_interface = ipaddress.IPv4Interface(local_ip + '/' + subnet_mask)
	print(ip_interface.network)

	print("Scanning...")
	# self.modbus_scan()
	clients_with_port_502_open= []

	if False:
		for ip in ip_interface.network:
			print(ip)
			port=502
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(1)
			result = sock.connect_ex((str(ip), port))
			if result == 0:
				clients_with_port_502_open.append(ip)
			sock.close()

	clients_with_port_502_open.append("10.0.0.142")
	print(clients_with_port_502_open)

	print("\n\nReading device info")
	for ip in clients_with_port_502_open:
		print(ip)
		try:
			x = 1
			client = pymodbus.client.ModbusTcpClient(ip)
			result = client.read_device_information()
			print(result.information)
		except:
			print("no information")
		print(ip)

	print("...Scanning Complete")

	# ModbusMemory Map
	# self.read_modbus_mmeory()
	client = pymodbus.client.ModbusTcpClient(ip)
	memory_map = {}
	for address in range(0, 20):
		try:
			if 0 <= address < 10000: # Discrete Outputs
				result = client.read_coils(address, 1)
				print(result.bits[0])
			else: # Discrete Inputs
				result = client.read_discrete_inputs(address - 10000,1)
			if result.bits[0]:
				memory_map[address] = True
		#except pymodbus.ModbusIOException:
		except:
			print("*** Exception ***")
			pass
	client.close()
	print(memory_map)

def myTest():
	print("My Test")

def myMap():
	print("My Map")

def myDefine():
	print("My Define")

################### Main #######################

def main():
	options = get_arguments()
	#print(options)

	if (options.modbus != None):
		if (options.modbus == 'server'):
			svr = MyModbusServer()
			svr.modbus_server()
		elif (options.modbus == 'client'):
			client = MyModbusClient()
			client.run()
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
	#print(sys.version)
	main()
	#hack()


