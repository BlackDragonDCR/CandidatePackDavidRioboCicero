import os
import uuid
import json
from flask_cors import CORS
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = './data/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

META_FILE = './data/images_meta.json'

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    #check the file exists
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    #check file selection is valid
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    #make unique ID for image
    original_name = secure_filename(file.filename)
    extension = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else 'jpg'
    image_id = f"{uuid.uuid4().hex}.{extension}"
    image_path = os.path.join(UPLOAD_DIR, image_id)
    
    #save the file
    file.save(image_path)
    
    #save metadata
    if os.path.exists(META_FILE):
        with open(META_FILE, 'r') as meta_file:
            meta = json.load(meta_file)
    else:
        meta = {}
        
    meta[image_id] = {
        "original_name": original_name,
        "uploaded_at": datetime.now().isoformat()
    }

    with open(META_FILE, 'w') as meta_file:
        json.dump(meta, meta_file)

    return jsonify({
        "message": "Image uploaded successfully",
        "image_id": image_id
    })

@app.route('/api/list_images', methods=['GET'])
def list_images():
    #check directory existance
    if not os.path.exists(META_FILE):
        return jsonify({"items": []})
    
    with open(META_FILE, 'r') as meta_file:
        meta = json.load(meta_file)
    
    items = []
    for image_id, info in meta.items():
        #check if files actually exist
        if os.path.exists(os.path.join(UPLOAD_DIR, image_id)):
            items.append({
                "image_id": image_id,
                "url": f"/uploads/{image_id}"
            })

    return jsonify({"items": items})

@app.route('/uploads/<path:filename>')
def serve_upload (filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)