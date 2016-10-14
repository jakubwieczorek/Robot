import ev3dev.ev3 as ev3

class Controller:
	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outA')
		self.rightMotor = ev3.LargeMotor('outD')
		self.colorSensor = ev3.ColorSensor('in1')

	def goForward(self, leftSpeed = -300, rightSpeed = -300, time = None):
		#ev3.Sound.speak('Go go go').wait()
		
		if time == None:	
			self.rightMotor.run_forever(speed_sp = rightSpeed)
			self.leftMotor.run_forever(speed_sp = leftSpeed)
		else:	
			self.leftMotor.run_timed(time_sp = 3000, speed_sp = leftSpeed)
			self.rightMotor.run_timed(time_sp = 3000, speed_sp = rightSpeed)

	def turnRight(self, speed = -300):
		self.stop()
		self.leftMotor.run_forever(speed_sp = speed)
	
	def turnLeft(self, speed = -300):
		self.stop()
		self.rightMotor.run_forever(speed_sp = speed)
			
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
		turn = self.turnRight
		turnTheOtherSide = self.turnLeft
		
		while True:
			if self.detectColor() == "Black":
				turn()
			elif self.detectColor() == "White": # if detected color is white, robot must turn to the other side
				while self.detectColor == "White": # if is white robot must turn till he won't achieve black color again
					turnTheOtherSide()
				
				""" now we must change functions, in order to when robot just achieve black color he must turning to the
				same direction""" 
				temp = turn 
				turn = turnTheOtherSide
				turnTheOtherSide = temp

robot = Controller()

robot.followTheLine()

