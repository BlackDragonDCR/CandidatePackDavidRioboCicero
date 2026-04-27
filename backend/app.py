from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = './data/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    original_name = secure_filename(file.filename)
    extension = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    image_id = f"{uuid.uuid4().hex}.{extension}"
    image_path = os.path.join(UPLOAD_DIR, image_id)
    
    file.save(image_path)
    
    return jsonify({
        "message": "Image uploaded successfully",
        "image_id": image_id
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)