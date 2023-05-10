
# Modbus Lib
# Anvindh Kumar
	
# Attachments12:43 PM (30 minutes ago)
	
# to Vikram, Manjunatha, me
# 2 Attachments
	
	
	

from pymodbus.client.sync import ModbusTcpClient as MC

def singleton(cls):
	instances = {}
	def getinstance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return getinstance

@singleton
class ModbusController():
	def __init__(self):
		#uid : unique identification (example: ip address for Modbus TCP and VID:HWID for Modbus ASCII/RTU)
		self.timeout = 1
		self.parity = 'E'
		self.stopbits = 1
		self.bytesize = 7
		self.baudrate = 9600

	def connect(self,uid,**kwargs):
		self.controller = self.establish_connection(uid,kwargs)
		if self.controller != None:
			print('Modbus Connection Established')
			return True
		else :
			print('Modbus Connection Failed')
			return False

	def fetch_port(self,uid):
		for port,pid,hwid in sorted(list_ports.comports()):
			try:
				if ((hwid.split())[1].split('='))[1] == uid:
					print(port)
					return port
			except e as Exception:
				print(e,', Exception occured for :', hwid)

	def set(self,key,value):
		if key == 'timeout':
			self.timeout = value
		elif key == 'parity':
			self.parity = value
		elif key == 'stopbits':
			self.stopbits = value
		elif key == 'bytesize':
			self.bytesize = value
		elif key == 'baudrate':
			self.baudrate = value

	def get(self,key):
		if key == 'timeout':
			return self.timeout
		elif key == 'parity':
			return self.parity
		elif key == 'stopbits':
			return self.stopbits
		elif key == 'bytesize':
			return self.bytesize
		elif key == 'baudrate':
			return self.baudrate
		
	def establish_connection(self, uid, kwargs):
		if kwargs['mode']=='TCP':
			client = MC(uid, port=502,timeout=self.timeout)
		elif kwargs['mode'] == 'ASCII':
			client=MC(method='ascii',port=self.fetch_port(uid),timeout=self.timeout,parity=self.parity,stopbits=self.stopbits,bytesize=self.bytesize,baudrate=self.baudrate)
		status = client.connect()
		if status == True:
			return client


	def write_holding_register(self, address, val):
		try:
			data = self.controller.write_register(address, val, unit=0x1)
			return (not data.isError())
		except Exception as e:
			return e

	def read_holding_register(self, address):
		try:
			data=self.controller.read_holding_registers(address, 1, unit=0x1)
			# x = not data.isError()
			if data.isError() == False:
				return data.registers[0]
			else:
				return None
		except Exception as e:
			return e

	def write_coil(self,address, val):
		try:
			data = self.controller.write_coil(address, val, unit=0x1)
			return (not data.isError())
		except Exception as e:
			return e

	def read_coil(self, address):
		try:
			data=(self.controller.read_coils(address, 1, unit=0x1))
			# x = not data.isError()
			if data.isError() == False:
				return data.bits[0]
			else:
				return None
		except Exception as e:
			return e

	def read_discrete_input(self, address):
		try:
			data=controller.read_discrete_inputs(address, 1, unit=0x1)
			# x = not data.isError()
			if data.isError() == False:
				return data.bits[0]
			else:
				return None
		except Exception as e:
			return e

	def read_input_register(self, address):
		try:
			data=controller.read_input_registers(address, 1, unit=0x1)
			# x = not data.isError()
			if data.isError() == False:
				return data.bits[0]
			else:
				return None
		except Exception as e:
			return e
