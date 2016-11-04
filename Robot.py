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
		self.frontColorSensor = ev3.ColorSensor('in2')

	def goForward(self, leftSpeed = 100, rightSpeed = 100, time = None):
		if time == None:	
			self.rightMotor.run_forever(speed_sp = rightSpeed)
			self.leftMotor.run_forever(speed_sp = leftSpeed)
		else:	
			self.leftMotor.run_timed(time_sp = time, speed_sp = leftSpeed)
			self.rightMotor.run_timed(time_sp = time, speed_sp = rightSpeed)

	def turnRight(self, speed = 100):
		self.stop()
		self.rightMotor.run_forever(speed_sp = 0)
		self.leftMotor.run_forever(speed_sp = speed)
	
	def turnLeft(self, speed = 100):
		self.stop()
		self.leftMotor.run_forever(speed_sp = 0)
		self.rightMotor.run_forever(speed_sp = speed)
			
	def readColor(self, sensor):	
		return sensor.color()

	def stop(self):
		self.leftMotor.stop()
		self.rightMotor.stop()

	def detectColor(self, sensor):
		color = self.readColor(sensor)

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
		speed = 150
		
		while True:
			light = self.detectLightness()
			self.goForward(speed * float((1 + self.turn(light))), speed * float((1 - self.turn(light))))
	def __del__(self):
		self.stop()	
	
	def turn(self, inputPos):
		currentColor = self.detectColor(self.frontColorSensor)		

		print(currentColor)

		if currentColor == "Black":
			return 0		
		elif currentColor == "Red":
			self.drag()	

		a = 2.0 / (self.minLightness - self.maxLightness)
		error = inputPos - (self.minLightness + self.maxLightness) / 2
	
		if self.integral > -7000:
			self.integral = self.integral + error
		else:
			self.integral = -pow(abs(self.integral), 0.5)
	
		derivative = error - self.prevError
		Ki = 0.01
		Kd = 0.5
		return a * (error + Ki * self.integral + Kd * derivative) 
	
	def drag(self):
		self.goForward(100, 100)		

		Time.sleep(1.2) # line between two wheels
			
		self.goForward(100, -100) # first turn right
		
		Time.sleep(1.5) # block in fornt of robot
		
		if self.detectColor(self.frontColorSensor) == "White" and self.detectColor(self.colorSensor) == "White": # but if he turned to wrong side
			self.goForward(-100, 100)
			Time.sleep(2.85)
		
		self.goForward(0,0)

		while True:
			pass
							
robot = Controller()

robot.followTheLine()

#while True:
#	print(robot.detectLightness())
