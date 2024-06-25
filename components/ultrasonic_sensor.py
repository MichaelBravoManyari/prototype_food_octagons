import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, distance_threshold):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.distance_threshold = distance_threshold
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def measure_distance(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        
        startTime = time.time()
        stopTime = time.time()
    
        while GPIO.input(self.echo_pin) == 0:
            startTime = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
            stopTime = time.time()
        
        timeElapsed = stopTime - startTime
        dist = (timeElapsed * 34300) / 2
        
        return dist
    
    def average_distance(self):
        distances = []
        for _ in range(4):
            dist = self.measure_distance()
            distances.append(dist)
            time.sleep(0.02)
        return sum(distances) / len(distances)
    
    def isObjectDetected(self):
        dist = self.average_distance()
        #print("trigger_ping", self.trigger_pin, "distance:", dist, "cm")
        if (dist < self.distance_threshold):
            print("Se detecto un objeto")
        return dist < self.distance_threshold