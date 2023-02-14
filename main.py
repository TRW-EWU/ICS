#!/usr/bin/env/python3

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import argparse

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--aaa", dest="aaa", help="This is A???")
	arguments = parser.parse_args()
	# if not arguments.aaa:
		# parser.error("[-] Please specify arg 'aaa' .")
	return arguments

print("TIP ICS");

options = get_arguments()
if options.aaa:
	print(options.aaa)
else:
	print("Option aaa not entered")

print("Modbus Server ....")

store = ModbusSlaveContext(
   di = ModbusSequentialDataBlock(0, [17]*100), # digital inputs
   co = ModbusSequentialDataBlock(0, [17]*100), # coil outputs
   hr = ModbusSequentialDataBlock(0, [17]*100), # holding registers
   ir = ModbusSequentialDataBlock(0, [17]*100)) # ????

context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'PyModbus Inc.'
identity.ProductCode = 'PM'
identity.VendorUrl = 'https://github.com/riptideio/pyModbus'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'PyModbus'
identity.MajorMinorRevision = '1.0'

StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))
