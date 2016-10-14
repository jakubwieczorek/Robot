import ev3dev.ev3 as ev3

class Controller:
	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outA')
		self.rightMotor = ev3.LargeMotor('outD')
		self.colorSensor = ev3.ColorSensor('in1')

	def goForward(self, speed = -300, time = None):
		#ev3.Sound.speak('Go go go').wait()
		
		if time == None:	
			self.leftMotor.run_forever(speed_sp = speed)
			self.rightMotor.run_forever(speed_sp = speed)
		else:	
			self.leftMotor.run_timed(time_sp = 3000, speed_sp = speed)
			self.rightMotor.run_timed(time_sp = 3000, speed_sp = speed)

	def readColor(self):	
		return self.colorSensor.color()

	def stop(self):
		self.leftMotor.stop()
		self.rightMotor.stop()

	def showDetectedColor(self):
       		color = self.readColor()

        	if color == 0:
                	print("None")
        	elif color == 1:
               		print("Black")
        	elif color == 2:
               		print("Blue")
       		elif color == 3:
               		print("Green")
       		elif color == 4:
               		print("Yellow")
       		elif color == 5:
               		print("Red")
       		elif color == 6:
               		print("White")
       		elif color == 7:
               		print("Brown")
	
	def detectColor(self):
		color = self.readColor()

		if color == 0:
			return "None"
		elif color == 1:
			return "Black"
		elif color == 2:
			return "Blue"
		elif color == 3:
			return "Green"
		elif color == 4:
			return "Yellow"
		elif color == 5:
			return "Red"
		elif color == 6:
			return "White"
		elif color == 7:
			return "Brown"

	def followTheLine(self):
		while True:
			if self.detectColor() == "Black":
				self.goForward()
			else:
				self.stop()
			
			

robot = Controller()

robot.followTheLine()



