#!/usr/bin/env/python3

import argparse
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

################### Main #######################

def main():
	options = get_arguments()

	if (options.server != None):
		if (options.server == 'modbus'):
			svr = MyModbusServer()
			svr.modbus_server()

	if (options.client != None):
		if (options.client == 'modbus'):
			svr = MyModbusClient()
			svr.modbus_client()

if __name__ == '__main__':
	print(sys.version)
	main()



