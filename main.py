import RPi.GPIO as GPIO
from components.ultrasonic_sensor import UltrasonicSensor
from components.servo_motor import ServoMotor
from components.pi_camera import PiCamera
from identification.detection import OctagonPackageDetector
from comunication.data_transfer import FirebaseDataUploader
import config
import utils
from servo_controller import ServoController
import time
import asyncio
import os

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
async def detectAndUpload(ultrasonicSensor1, ultrasonicSensor2, servoController, camera, detector, firebaseUploader):
    try:
        while True:
            if ultrasonicSensor1.isObjectDetected() or ultrasonicSensor2.isObjectDetected():
                await asyncio.sleep(0.5)
                startTime = asyncio.get_event_loop().time()
                endTime = asyncio.get_event_loop().time()
                image = camera.captureImage()
                boxes, classNames, scores = detector.detectObjects(image)
                filtered_data = [(box, className, score) for box, className, score in zip(boxes, classNames, scores) if score > 0.1]
                if filtered_data:
                    filtered_boxes, filtered_classNames, filtered_scores = zip(*filtered_data)
                    if "VACIO" not in filtered_classNames:
                        # Save image
                        imageName = utils.generateUniqueFilename()
                        await firebaseUploader.uploadImage(image, imageName)
                        upload_tasks = []
                        for box, className, score in zip(filtered_boxes, filtered_classNames, filtered_scores):
                            if score >= 0.9:
                                upload_tasks.append(firebaseUploader.uploadData(imageName, box, className, score))
                            else:
                                upload_tasks.append(firebaseUploader.uploadData(imageName, box, "OTROS", score))
                        await asyncio.gather(*upload_tasks)
                        endTime = asyncio.get_event_loop().time()
                        servoController.openGate()
                        print("time:", (endTime - startTime) + 1.5)
            await asyncio.sleep(0.5)  
    except asyncio.CancelledError:
        print("Cancelled async tasks during shutdown")
    finally:
        servoController.stopServos()
        camera.stopCamera()
        GPIO.cleanup() 
    
async def main():
    setup()

    ultrasonicSensor1 = UltrasonicSensor(config.ULTRASONIC_SENSOR1_TRIGGER_GPIO, config.ULTRASONIC_SENSOR1_ECHO_GPIO, config.ULTRASONIC_SENSOR1_THRESHOLD_DISTANCE)
    ultrasonicSensor2 = UltrasonicSensor(config.ULTRASONIC_SENSOR2_TRIGGER_GPIO, config.ULTRASONIC_SENSOR2_ECHO_GPIO, config.ULTRASONIC_SENSOR2_THRESHOLD_DISTANCE)
    gateServoMotor = ServoMotor(config.SERVO_GATE_GPIO, config.SERVO_MOTOR_FREQUENCY)
    lockServoMotor = ServoMotor(config.SERVO_LOCK_GPIO, config.SERVO_MOTOR_FREQUENCY)
    servoController = ServoController(gateServoMotor, lockServoMotor)
    camera = PiCamera()
    detector = OctagonPackageDetector(config.MODEL_PATH, config.MODEL_LABELS, config.WARMUP_IMAGES_FOLDER)
    firebaseUploader = FirebaseDataUploader(config.FIREBASE_CRED_PATH, config.STORAGE_BUCKET_NAME)
    #Reiniciar servomotores
    servoController.openGate()
    
    #Archivo de señalización
    with open('/tmp/prototype_started', 'w') as f:
        f.write('started')
    
    await detectAndUpload(ultrasonicSensor1, ultrasonicSensor2, servoController, camera, detector, firebaseUploader)
            
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (asyncio.CancelledError, KeyboardInterrupt):
        print("Measurement stopped by user")