
import cv2
import numpy as np
from keras.models import load_model
import os
from glob import glob
from connectGPT import emotionResponseGenerator


def get_most_recent_image():
    folder_path = "./static/image/"
    files = glob(os.path.join(folder_path, '*'))
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0] if files else None



def emotion_label():
    model = load_model('model_file_30epochs.h5')
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    labels_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}

    # Assuming get_most_recent_image() returns the path to the most recent image
    image_path = get_most_recent_image()
    frame = cv2.imread(image_path, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 3)
    for x, y, w, h in faces:
            sub_face_img = gray[y:y+h, x:x+w]
            resized = cv2.resize(sub_face_img, (48, 48))
            normalize = resized / 255.0
            reshaped = np.reshape(normalize, (1, 48, 48, 1))
            result = model.predict(reshaped)
            label = np.argmax(result, axis=1)[0]
    
            # Mapping integer label to emotion string using labels_dict
            emotion_string = labels_dict.get(label, "Unknown")
            result_emotion = emotionResponseGenerator(emotion_string)
        
   
        
    return result_emotion




      





