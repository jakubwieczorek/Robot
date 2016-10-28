import ev3dev.ev3 as ev3
import time as Time

class Controller:
	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outA')
		self.rightMotor = ev3.LargeMotor('outD')
		self.colorSensor = ev3.ColorSensor('in1')
		self.colorSensor.mode = 'COL-REFLECT'
		self.maxLightness = 72.0
		self.minLightness = 7.0
		self.integral = 0
		self.prevError = 0
	def goForward(self, leftSpeed = 100, rightSpeed = 100, time = None):
		if time == None:	
			self.rightMotor.run_forever(speed_sp = rightSpeed)
			self.leftMotor.run_forever(speed_sp = leftSpeed)
		else:	
			self.leftMotor.run_timed(time_sp = 3000, speed_sp = leftSpeed)
			self.rightMotor.run_timed(time_sp = 3000, speed_sp = rightSpeed)

	def turnRight(self, speed = 100):
		self.stop()
		self.rightMotor.run_forever(speed_sp = 0)
		self.leftMotor.run_forever(speed_sp = speed)
	
	def turnLeft(self, speed = 100):
		self.stop()
		self.leftMotor.run_forever(speed_sp = 0)
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
		speed = 200
			
		time = 0.0
		
		while True:
			light = self.detectLightness()
			"""
			if light > 50 and time == 0.0:
				time = Time.time()

			if light < 25:
				time = 0.0

			if time - Time.time() > -5 and light > 50:
				self.turnRight()
				while self.detectLightness() > 26:
					pass
				time  = 0.0
				light = self.detectLightness()
			"""
			self.goForward(speed * float((1 + self.turn(light))), speed * float((1 - self.turn(light))))
	def __del__(self):
		self.stop()	
	
	def turn(self, inputPos):
		a = 2.0 / (self.minLightness - self.maxLightness)
		error = inputPos - (self.minLightness + self.maxLightness) / 2
	
		if self.integral > -7000:
			self.integral = self.integral + error
		else:
			self.integral = -pow(abs(self.integral), 0.5)
	
		print(self.integral)
			
		derivative = error - self.prevError
		Ki = 0.01
		Kd = 0.5
		return a * (error + Ki * self.integral + Kd * derivative) 
			
									
robot = Controller()

robot.followTheLine()

#while True:
#	print(robot.detectLightness())
