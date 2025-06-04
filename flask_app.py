from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import torch
from transformers import ViTForImageClassification
import pickle
import io
import os

app = Flask(__name__)

# Load the model and feature extractor
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ViTForImageClassification.from_pretrained(
    'google/vit-base-patch16-224-in21k',
    num_labels=2,
    ignore_mismatched_sizes=True
)
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(0.4),
    torch.nn.Linear(model.classifier.in_features, 2)
)
checkpoint = torch.load('vit_model.pt', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

with open('vit_feature_extractor.pkl', 'rb') as f:
    feature_extractor = pickle.load(f)

# Class labels
labels = {0: 'Autistic', 1: 'Non-Autistic'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        # Load and preprocess image
        image_file = request.files['image']
        image = Image.open(image_file).convert('RGB')
        
        # Preprocess image with feature extractor
        encoding = feature_extractor(images=image, return_tensors="pt")
        pixel_values = encoding['pixel_values'].to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(pixel_values=pixel_values).logits
            pred = torch.argmax(outputs, dim=1).cpu().numpy()[0]
        
        # Return prediction
        return jsonify({
            'prediction': labels[pred],
            'class_id': int(pred)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
