from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

class MyModbusServer:
    def __init__(self):
        # TRW: Does not appear to read 1st element in DataBlock
        self.coil_out = ModbusSequentialDataBlock(0, [0, 1,0,1,1,0,0,1,1,1,0,0,0]) # DigOut
        self.dig_in = ModbusSequentialDataBlock(0,   [0, 0,1,0,0,1,1,0,0,0,1,1,1]) # DigIn
        self.input_reg = ModbusSequentialDataBlock(0,   [0,  1,3,5,7,9,11,13,15,17,19]) # AnIn                 # 30 0001
        self.holding_reg = ModbusSequentialDataBlock(0, [0,  2,4,6,8,10,12,14,16,18,20]) # AnOut

    def modbus_server(self):
        print("Modbus Server ....")
        self.store = ModbusSlaveContext(
            di = self.dig_in,
            co = self.coil_out,
            hr = self.holding_reg,
            ir = self.input_reg)
        self.context = ModbusServerContext(slaves=self.store, single=True)

        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'ModbusTagServer'
        self.identity.ProductCode = 'PM'
        self.identity.VendorUrl = 'https://github.com/riptideio/pyModbus'
        self.identity.ProductName = 'Modbus Server'
        self.identity.ModelName = 'PyModbus'
        self.identity.MajorMinorRevision = '1.0'

        self.svr = StartTcpServer(context=self.context, identity=self.identity, 
                                    address=("0.0.0.0", 502))

if __name__ == '__main__':
	svr = MyModbusServer()
	svr.modbus_server()
