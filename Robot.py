import ev3dev.ev3 as ev3
import time as Time

class Controller:
	def __init__(self):
		self.leftMotor = ev3.LargeMotor('outA')
		self.rightMotor = ev3.LargeMotor('outD')
		self.colorSensor = ev3.ColorSensor('in1')
		self.colorSensor.mode = 'COL-REFLECT'
		self.maxLightness = 70.0
		self.minLightness = 8.0
		self.integral = 0
		self.prevError = 0
		self.frontColorSensor = ev3.ColorSensor('in4')
		self.mediumMotor = ev3.MediumMotor('outB')
		self.withCube = False	
	def pickUp(self):
		self.mediumMotor.run_forever(speed_sp = 400)
		Time.sleep(1)
		self.mediumMotor.stop()
	
	
	def drop(self):
                self.mediumMotor.run_forever(speed_sp = -400)
                Time.sleep(1)
                self.mediumMotor.stop()

	def goForward(self, leftSpeed = 100, rightSpeed = 100, time = None):
		if time == None:	
			self.rightMotor.run_forever(speed_sp = rightSpeed)
			self.leftMotor.run_forever(speed_sp = leftSpeed)
		else:	
			self.leftMotor.run_timed(time_sp = time, speed_sp = leftSpeed)
			self.rightMotor.run_timed(time_sp = time, speed_sp = rightSpeed)
	
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
		speed = -100
		
		while True:
			light = self.detectLightness()
			self.goForward(speed * float((1.0 + self.turn(light))), speed * float((1.0 - self.turn(light))))
	
	def __del__(self):
		self.stop()	
	
	def turn(self, inputPos):
		currentColor = self.detectColor(self.frontColorSensor)		

		print(currentColor)

		if currentColor == "Black":
			return 0
 
		elif currentColor == "Red" and self.withCube == False:
			self.drag(self.pickUp)
			return 0

		elif currentColor == "Green" and self.withCube == True:
			self.drag(self.drop)
			return 0
		
		a = 2.0 / (self.minLightness - self.maxLightness)
		error = inputPos - (self.minLightness + self.maxLightness) / 2

		derivative = error - self.prevError
		Kd = 0.2
		Kp = 0.8

		return a * (Kp * error + Kd * derivative)
	
	def drag(self, upOrDown):
		self.goForward(-100, -100)		

		Time.sleep(3) # line between two wheels
			
		self.goForward(-100, 100) # first turn right
		
		Time.sleep(1.8) # block in fornt of robot
	
		if self.detectColor(self.frontColorSensor) == "White" and self.detectColor(self.colorSensor) == "White": # but if he turned to wrong side
			pass
		else:
			self.goForward(-100, 100)
			Time.sleep(3.4)
		
		self.goForward(100, 100)
		Time.sleep(3.0)
		
		upOrDown()
		
		self.goForward(-100, -100)
		Time.sleep(3)
		
		self.goForward(100, -100)
		
		while self.detectColor(self.frontColorSensor) != "Black":
			pass
		
		self.stop()
			
		self.withCube =not self.withCube	

if __name__ == "__main__":							
	robot = Controller()


	robot.followTheLine()
	#while True:
	#	print(robot.detectLightness())
	#	print(robot.detectColor(robot.frontColorSensor))
	#	print(robot.infraredSensor.proximity())
