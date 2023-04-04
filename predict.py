import tensorflow as tf
import numpy as np
from PIL import Image
import gradio as gr

tf.config.run_functions_eagerly(False)

# Load the trained model for auto claim prediction
model = tf.keras.models.load_model('auto_claim_model.h5')

# Define a function to preprocess the image before feeding it to the model
def preprocess_image(img):
    # Resize the image to 224x224 pixels
    img = img.resize((224, 224))
    # Convert the image to a NumPy array
    img_array = np.array(img)
    # Convert the pixel values from 0-255 to -1.0 to 1.0
    img_array = img_array / 127.5 - 1.0
    # Expand the dimensions of the image to match the input shape of the model
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Define a function to make the prediction using the loaded model
def predict_auto_claim(image, policy_number, threshold=0.5):
    # Preprocess the image
    img_array = preprocess_image(image)
    # Make the prediction
    prediction = model.predict([img_array, np.array([policy_number])])
    # Get the predicted probability of auto claim
    auto_claim_prob = prediction[0][0]
    # Return 1 if probability is greater than or equal to the threshold, else return 0
    return int(auto_claim_prob >= threshold)


inputs = [
    gr.inputs.Image(type='pil', label='Upload Image'),
    gr.inputs.Number(label='Policy Number'),
    gr.inputs.Slider(minimum=0, maximum=1, step=0.01, default=0.5, label='Threshold')
]
output = gr.outputs.Label(num_top_classes=1, label='Auto Claim Prediction')
interface = gr.Interface(fn=predict_auto_claim, inputs=inputs, outputs=output, title='Auto Claim Prediction')
interface.launch()

