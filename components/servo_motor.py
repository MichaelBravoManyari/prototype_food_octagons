import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pwm_pin, frequency):
        self.pwm_pin = pwm_pin
        self.frequency = frequency
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.pwm.start(0)
        
    def rotateTo(self, angle):
        # Convierte el angulo en un ciclo de trabajo (duty cycle)
        duty_cycle = (angle / 18.0) + 2
        self.pwm.ChangeDutyCycle(duty_cycle)
    
    def stopServoPulse(self):
        # Detener el pulso para evitar que el servo zumbe
        self.pwm.ChangeDutyCycle(0)
        
    def stopServo(self):
        self.pwm.stop()