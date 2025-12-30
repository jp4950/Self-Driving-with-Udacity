from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import cv2
import base64

MODEL_PATH = "saved_model.keras"
MAX_SPEED = 30.0

app = Flask(__name__)

print(f"Loading model from {MODEL_PATH} ...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded successfully!")

def preprocess_image(img_bgr):
    """Crop, resize, and normalize the image like during training."""
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img = img[75:135, :, :]   # remove sky and hood
    img = cv2.resize(img, (320, 60))
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)

@app.route("/predict", methods=["POST"])
def predict():
    """Receive telemetry JSON and return steering/throttle."""
    try:
        data = request.get_json(force=True)
        image_str = data.get("image")
        speed = float(data.get("speed", 0.0))

        # Decode base64 image
        img_bytes = base64.b64decode(image_str)
        np_img = np.frombuffer(img_bytes, np.uint8)
        img_bgr = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Predict
        img = preprocess_image(img_bgr)
        steering = float(model.predict(img, verbose=0)[0][0])
        throttle = max(0.0, 1.0 - speed / MAX_SPEED)

        print(f"Predicted: steering={steering:.4f}, throttle={throttle:.4f}, speed={speed:.2f}")
        return jsonify({"steering_angle": steering, "throttle": throttle})
    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return "Model API is running", 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)