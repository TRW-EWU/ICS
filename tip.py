#!/usr/bin/env/python3

import argparse
import sys

from MyModbusServer import MyModbusServer
#from MyModbusClient import MyModbusClient

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
	#print(options)
	#print(options.server)
	#print(options.client)

	if (options.server != None):
		if (options.server == 'modbus'):
			svr = MyModbusServer()
			svr.modbus_server()
			pass

	if (options.client != None):
		if (options.client == 'modbus'):
			#svr = MyModbusClient()
			#print(svr.x)
			#svr.modbus_client()
			pass

if __name__ == '__main__':
	print(sys.version)
	main()



