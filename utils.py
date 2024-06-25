import uuid
import time

def generateUniqueFilename():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    unique_id = str(uuid.uuid4())
    image_name = f"captura_{timestamp}_{unique_id}.jpg"
    return image_name