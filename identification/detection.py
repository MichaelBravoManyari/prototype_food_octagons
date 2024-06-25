from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
import os

class OctagonPackageDetector:
    def __init__(self, model_path, labels, warmup_images_folder):
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.labels = labels
        self.warmUpInference(warmup_images_folder)
       
    def warmUpInference(self, warmup_images_folder):
        input_shape = self.input_details[0]['shape']
        for image_path in os.listdir(warmup_images_folder):
            if image_path.endswith(".jpg") or image_path.endswith(".png"):
                image = cv2.imread(os.path.join(warmup_images_folder, image_path))
                input_data = self.preprocessImage(image)
                self.setInputTensor(input_data)
                self.invokeInterpreter() 
       
    def preprocessImage(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_shape = self.input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]
        image_resized = cv2.resize(image, (width, height))
        image_normalized = (np.float32(image_resized) - 127.5) / 127.5
        return np.expand_dims(image_normalized, axis=0)
    
    def setInputTensor(self, input_data):
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
    
    def invokeInterpreter(self):
        self.interpreter.invoke()
        
    def getOutputTensors(self):
        boxes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        class_indices = self.interpreter.get_tensor(self.output_details[3]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        return boxes, class_indices, scores
    
    def detectObjects(self, image):
        input_data = self.preprocessImage(image)
        self.setInputTensor(input_data)
        self.invokeInterpreter()
        boxes, class_indices, scores = self.getOutputTensors()
        class_names = [self.labels[int(index)] for index in class_indices]
        return boxes, class_names, scores