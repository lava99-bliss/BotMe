import os 
import time
from connectGPT import chatResponseGenerator
from flask import send_file,Flask, render_template, request, jsonify
from chat import get_response
from testdata import emotion_label
import random
from objectDetect import detect_object

# from connectGPT import emotionResponseGenerator

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html")



image_folder = "./PhotoChat/"

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            text = data.get("message")
            print(text)
            
            # Check if the user's message contains a request for an image
            if any(keyword in text.lower() for keyword in ["image", "capture","snap","photo", "send me an image", "an image please"]):
                # List all files in the image folder
                image_files = os.listdir(image_folder)
                
                # Select a random image
                random_image = random.choice(image_files)
                image_path = os.path.join(image_folder, random_image)
                
                print(detect_object(image_path))

                # Return the image data as a response
                return send_file(image_path, mimetype='image/jpeg')
            else:
                # Process the query using the chatResponseGenerator function
                response = chatResponseGenerator(text)
                print(response.content)
                message = {"answer": response.content}
                return jsonify(message)
        else:
            return jsonify({"error": "Invalid request, must be in JSON format"})

@app.route("/uploadImage", methods=["POST"])
def upload_image():
    try:
        if request.method == "POST":
            # message={"answer":"Hey, I noticed you seem a bit neutral today. Is everything okay? If you feel like talking about it, I'm here to listen. Sometimes we have moments where we just feel neutral, and that's totally normal. Just know that whatever you're going through, it's okay to feel the way you do. Take some time for yourself and do something that brings you comfort or joy. Remember, I'm here for you if you need someone to talk to."}
            # return jsonify(message)
            
            if "image" in request.files:
                image = request.files["image"]
                image_folder = "static\image"
                if not os.path.exists(image_folder):
                    os.makedirs(image_folder)

                image_path = os.path.join(image_folder, image.filename)
                
                image.save(image_path)
                return jsonify({"answer": "emotion"})
            
            else:
                emotion = emotion_label()
                print(emotion.content)

                print("This is else")
                message = {"answer": emotion.content}
                return jsonify(message)
                # return jsonify({"error": "No image uploaded"})
        else:
            return jsonify({"error": "Invalid request method"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/image/emotion-detection", methods=["POST"])
def emotion_detection():
    try:
        if request.method == "POST":
             emotion = emotion_label()
            #  print(emotion.content)

             print("This is else")
             message = {"answer": emotion.content}
             return jsonify(message)
             # return jsonify({"error": "No image uploaded"})
               
        else:
            return jsonify({"error": "Invalid request method"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    





if __name__ == "__main__":
    app.run(debug=True)

