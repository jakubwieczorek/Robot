import ev3dev.ev3 as ev3

class Controller:
	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outA')
		self.rightMotor = ev3.LargeMotor('outD')
		self.colorSensor = ev3.ColorSensor('in1')
		self.colorSensor.mode = 'COL-REFLECT'

	def goForward(self, leftSpeed = -400, rightSpeed = -400, time = None):
		if time == None:	
			self.rightMotor.run_forever(speed_sp = rightSpeed)
			self.leftMotor.run_forever(speed_sp = leftSpeed)
		else:	
			self.leftMotor.run_timed(time_sp = 3000, speed_sp = leftSpeed)
			self.rightMotor.run_timed(time_sp = 3000, speed_sp = rightSpeed)

	def turnRight(self, speed = -300):
		self.stop()
		self.rightMotor.run_forever(speed_sp = -speed)
		self.leftMotor.run_forever(speed_sp = speed)
	
	def turnLeft(self, speed = -300):
		self.stop()
		self.leftMotor.run_forever(speed_sp = -speed)
		self.rightMotor.run_forever(speed_sp = speed)
			
	def readColor(self):	
		return self.colorSensor.color()

	def stop(self):
		self.leftMotor.stop()
		self.rightMotor.stop()

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
	def detectLightness(self):	
		return self.colorSensor.value()
	
	def followTheLine(self):
		turn = self.turnRight
		turnTheOtherSide = self.turnLeft
			
		turn()
		while True:
			if self.detectLightness() > 10:	
				# now we must change functions, in order to change engine
				temp = turn 
				turn = turnTheOtherSide
				turnTheOtherSide = temp
				
				turn()

				while self.detectLightness() > 6:
					pass
	def __del__(self):
		self.stop()	
		 
			
									
robot = Controller()

robot.followTheLine()
