

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

#
# modbus-cli
#
# modbus read <IP> %M1 -5
# modbus read <IP> 300001 1-10
# modbus read <IP> 400001 1-10
#

class MyModbusServer:
    def __init__(self):
        self.coil_out = ModbusSequentialDataBlock(0, [1, 0, 0, 1, 1, 0, 1, 1, 1]) # %M1 5
        self.holding_reg = ModbusSequentialDataBlock(0, [1,2,3,4,5,6,8]*10)       # 40 0001
        self.input_reg = ModbusSequentialDataBlock(0, [9, 0]*100)                 # 30 0001

    def modbus_server(self):
        print("Modbus Server ....")
        self.store = ModbusSlaveContext(
            di = ModbusSequentialDataBlock(0, [17]*100), # digital inputs
            co = self.coil_out,
            hr = self.holding_reg,
            ir = self.input_reg)
        self.context = ModbusServerContext(slaves=self.store, single=True)

        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'PyModbus Inc.'
        self.identity.ProductCode = 'PM'
        self.identity.VendorUrl = 'https://github.com/riptideio/pyModbus'
        self.identity.ProductName = 'Modbus Server'
        self.identity.ModelName = 'PyModbus'
        self.identity.MajorMinorRevision = '1.0'

        self.svr = StartTcpServer(context=self.context, identity=self.identity, 
                                    address=("10.101.68.70", 502))

