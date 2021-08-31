from threading import Thread 
import time
from serial import Serial
from abc import ABCMeta, abstractmethod

class ProcRxMsg(Thread):
	def __init__(self, ser, cmds):
		Thread.__init__(self)
		self.mSer = ser
		self.mClose = False
		self.mCmds = cmds

	def run(self):
		while not self.mClose:
			line = self.mSer.readline().decode("utf-8")
			try:
				cmd = self.mCmds[line.strip('\r\n')]
				cmd.execute()
			except KeyError:
				print(line.strip('\r\n'))
			
	def close(self):
		self.mClose = True

class ProcTxMsg(Thread):
	def __init__(self, ser, cmds):
		Thread.__init__(self)
		self.mSer = ser
		self.mClose = False
		self.mCmds = cmds.keys()

	def run(self):
		while not self.mClose:
			try:
				idx = int(input())
				cmd = list(self.mCmds)[idx] + "\r\n"
				self.mSer.write(cmd.encode('utf-8'))
			except ValueError:
				print('Input number!')
			except IndexError:
				print('Command not found')

	def close(self):
		self.mClose = True

class IAction:
	__metaclass__ = ABCMeta
	@abstractmethod
	def on(self):
		pass
	@abstractmethod
	def off(self):
		pass

class DLed(IAction):
	def __init__(self, name):
		self.mName = name
	def on(self):
		print(f"Action => {self.mName} LED On")
	def off(self):
		print(f"Action => {self.mName} LED Off")

class Buzzer(IAction):
	def __init__(self, name):
		self.mName = name
	def on(self):
		print(f"Action => {self.mName} On")
	def off(self):
		print(f"Action => {self.mName} Off")

class ICommand:
	__metaclass__ = ABCMeta
	@abstractmethod
	def execute(self):
		pass

class RedLedOnCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.on()
class RedLedOffCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.off()

class GreenLedOnCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.on()
class GreenLedOffCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.off()

class YellowLedOnCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.on()
class YellowLedOffCommand(ICommand):
	def __init__(self, led):
		self.mLed = led

	def execute(self):
		self.mLed.off()

class BuzzerOnCommand(ICommand):
	def __init__(self, buzzer):
		self.mBuzzer = buzzer

	def execute(self):
		self.mBuzzer.on()
class BuzzerOffCommand(ICommand):
	def __init__(self, buzzer):
		self.mBuzzer = led

	def execute(self):
		self.mBuzzer.off()

def initCmdList():
	cmdList = dict()

	redled = DLed('Red')
	greenled = DLed('Green')
	yellowled = DLed('Yellow')
	buzzer = Buzzer("Buzzer")

	cmdList["RedLed_ON"] = RedLedOnCommand(redled)
	cmdList["RedLed_OFF"] = RedLedOffCommand(redled)
	cmdList["GreenLed_ON"] = GreenLedOnCommand(greenled)
	cmdList["GreenLed_OFF"] = GreenLedOffCommand(greenled)
	cmdList["YellowLed_ON"] = YellowLedOnCommand(yellowled)
	cmdList["YellowLed_OFF"] = YellowLedOffCommand(yellowled)
	cmdList["Buzzer_ON"] = YellowLedOnCommand(buzzer)
	cmdList["Buzzer_OFF"] = YellowLedOffCommand(buzzer)
	
	return cmdList

def main():
	cmdList = initCmdList()
	ser = Serial('COM7', 19200, timeout=10)

	pRx = ProcRxMsg(ser, cmdList)
	pTx = ProcTxMsg(ser, cmdList)
	pRx.setDaemon(True)
	pTx.setDaemon(True)
	pRx.start()
	pTx.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		pRx.close()
		pTx.close()
		ser.close()


if __name__ == "__main__":
	main()
	
