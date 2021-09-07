from threading import Thread 
import time

class ThdClass(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.mStop = False

	def run(self):
		while not self.mStop:
			print("Thread class")
			time.sleep(1)

		print('Thread class done!!')
			
	def stop(self):
		self.mStop = True

def Thdfunction(name, stop):
	while not stop():
		print("Thread function")
		time.sleep(1)

	print('Thread function done!!')

def main():
	thdc = ThdClass()
	thdc.start()

	stop_thread = False
	thdf = Thread(target=Thdfunction, args=('thdf', lambda: stop_thread))
	thdf.start()

	try:
		while True:
			cmd = input()
			if(cmd =='q'):
				print('stopping.....')
				thdc.stop()
				stop_thread = True
				break;
			print('Main Thread')

	except KeyboardInterrupt:
		thdc.stop()
		stop_thread = True
	finally:
		thdf.join()
		thdc.join()

if __name__ == "__main__":
	main()