from picamera2 import Picamera2

class PiCamera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.start()
        
    def captureImage(self):
        image = self.picam2.capture_array()
        return image
    
    def stopCamera(self):
        self.picam2.stop()
    