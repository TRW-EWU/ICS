#!/usr/bin/env/python3

# OBSOLETE: Use tip.py as main program

import argparse
from MyModbusServer import MyModbusServer

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--server", dest="server", help="SERVER: modbus, profinet, s7")
	arguments = parser.parse_args()
	# if not arguments.aaa:
		# parser.error("[-] Please specify arg 'aaa' .")
	return arguments

################### Main #######################

def main():
	options = get_arguments()
	if options.server == 'modbus':
		svr = MyModbusServer()
		svr.modbus_server()
	else:
		print("Invalid server option: ", options.server)

if __name__ == '__main__':
	main()



