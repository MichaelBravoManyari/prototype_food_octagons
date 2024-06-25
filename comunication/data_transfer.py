import firebase_admin
from firebase_admin import credentials, firestore, storage
import cv2
import time
import asyncio
import concurrent.futures

class FirebaseDataUploader:
    def __init__(self, firebase_cred_path, storage_bucket_name):
        self._initialize_firebase(firebase_cred_path, storage_bucket_name)
        self.executor = concurrent.futures.ThreadPoolExecutor()
        
    def _initialize_firebase(self, firebase_cred_path, storage_bucket_name):
        self.cred = credentials.Certificate(firebase_cred_path)
        firebase_admin.initialize_app(self.cred, {'storageBucket': storage_bucket_name})
        self.db = firestore.client()
        self.bucket = storage.bucket()
        
    async def uploadImage(self, image, image_name):
        try:
            image_bytes = self._convert_image_to_bytes(image)
            await asyncio.wait_for(self._upload_to_storage(image_bytes, image_name), timeout=2)
        except asyncio.TimeoutError:
            print("Timeout: Error uploading image")
        except Exception as e:
            print(f"Error uploading image: {e}")
        
    def _convert_image_to_bytes(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _, image_encoded = cv2.imencode('.jpg', image)
        return image_encoded.tobytes()
        
    async def _upload_to_storage(self, image_bytes, image_name):
        try:
            blob = self.bucket.blob(image_name)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, blob.upload_from_string, image_bytes, 'image/jpeg')
        except Exception as e:
            print(f"Error uploading to storage: {e}")
        
    async def uploadData(self, image_name, box, class_name, score):
        try:
            metadata = self._create_metadata(image_name, box, class_name, score)
            print("Metadata: ", metadata)
            await asyncio.wait_for(self._save_to_firestore(metadata), timeout=2)
        except asyncio.TimeoutError:
            print("Timeout: Error uploading data")
        except Exception as e:
            print(f"Error uploading data: {e}")
        
    def _create_metadata(self, image_name, box, class_name, score):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        return {
            'class_name': class_name,
            'score': round(float(score), 2),
            'box': tuple(float(coord) for coord in box),
            'timestamp': timestamp,
            'image_name': image_name
        }
        
    async def _save_to_firestore(self, metadata):
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self.db.collection('detections').add, metadata)
        except Exception as e:
            print(f"Error saving to Firestore: {e}")