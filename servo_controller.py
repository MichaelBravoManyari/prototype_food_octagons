import time

class ServoController:
    def __init__(self, gate_servo_motor, lock_servo_motor):
        self.gate_servo_motor = gate_servo_motor
        self.lock_servo_motor = lock_servo_motor
        
    def openGate(self):
        self.lock_servo_motor.rotateTo(40)
        time.sleep(0.5)
        self.lock_servo_motor.stopServoPulse()
        self.gate_servo_motor.rotateTo(50)
        time.sleep(1)
        self.gate_servo_motor.rotateTo(0)
        time.sleep(0.5)
        self.lock_servo_motor.rotateTo(120)
        time.sleep(0.1)
        self.gate_servo_motor.stopServoPulse()
        self.lock_servo_motor.stopServoPulse()
        
    def stopServos(self):
        self.lock_servo_motor.stopServo()
        self.gate_servo_motor.stopServo()

        