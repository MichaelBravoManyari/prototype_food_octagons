#MODE BOARD
ULTRASONIC_SENSOR1_TRIGGER_GPIO = 16
ULTRASONIC_SENSOR1_ECHO_GPIO = 18
ULTRASONIC_SENSOR2_TRIGGER_GPIO = 22
ULTRASONIC_SENSOR2_ECHO_GPIO = 36
SERVO_GATE_GPIO = 12
SERVO_LOCK_GPIO = 32
SERVO_MOTOR_FREQUENCY = 50

#Limit distance of ultrasound sensors (cm)
ULTRASONIC_SENSOR1_THRESHOLD_DISTANCE = 20
ULTRASONIC_SENSOR2_THRESHOLD_DISTANCE = 18

#Model configuration
MODEL_PATH = "/home/maic753/python_scripts/prototipo_tesis_alimentos_octogonos/identification/tflite_model/detect.tflite"
QUANT_MODEL_PATH = "/home/maic753/python_scripts/prototipo_tesis_alimentos_octogonos/identification/tflite_model/detect_quant.tflite"
MODEL_LABELS = ("CEREAL_ANGEL_COPIX", "CHOCMAN_COSTA_28G", "CHOMP_CHOCOLATE_38G",
                       "CHOMP_NARANJA_38G", "GALLETA_RELLENITAS_CHOCOLATE_GN_6_GALLETAS",
                       "GALLETA_RELLENITAS_COCO_GN_6_GALLETAS", "GALLETA_RELLENITAS_FRESA_GN_6_GALLETAS",
                       "GALLETA_RITZ_8_GALLETAS", "GALLETA_OREO_4_GALLETAS", "PEPSI_500ML", "OTROS", "VACIO")
WARMUP_IMAGES_FOLDER = "/home/maic753/python_scripts/prototipo_tesis_alimentos_octogonos/identification/warmup_images"

#Firebase configuration
FIREBASE_CRED_PATH = "/home/maic753/python_scripts/prototipo_tesis_alimentos_octogonos/comunication/octogonos-en-alimentos-firebase-adminsdk-cuw6g-888c447736.json"
STORAGE_BUCKET_NAME = "octogonos-en-alimentos.appspot.com"
