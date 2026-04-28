import os
import uuid
import json
import hashlib
from PIL import Image
from flask_cors import CORS
from datetime import datetime, timedelta
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

@app.route('/api/analyse_image', methods=['POST'])
def analyse_image():
    #get and validate json
    data = request.get_json()
    if not data or 'image_id' not in data:
        return jsonify({"error": "image_id required"}), 400
    
    image_id = data['image_id']
    image_path = os.path.join(UPLOAD_DIR, image_id)

    #check if image exists
    if not os.path.exists(image_path):
        return jsonify({"error": "image not found"}), 400
    
    #analyse image with PIL
    try:
        img = Image.open(image_path)
        analysis = {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode,
            "size_kb": round(os.path.getsize(image_path) / 1024, 2)
        }
    except Exception as e:
        return jsonify({"error": f"failed to analyse image: {str(e)}"}), 500
    
    return jsonify({
        "image_id": image_id,
        "analysis": analysis
    })

#file for saving tokens
TOKENS_FILE ='./data/tokens.json'

@app.route('/api/share_image', methods=['POST'])
def share_image():
    #get and validate redieved json
    data = request.get_json()
    if not data or 'image_id' not in data:
        return jsonify({"error": "image_id required"}), 400
    
    image_id = data['image_id']
    image_path = os.path.join(UPLOAD_DIR, image_id)

    #check if image exists
    if not os.path.exists(image_path):
        return jsonify({"error": "image not found"}), 404
    
    #create unique token
    random_part = uuid.uuid4().hex[:8]
    timestamp = datetime.now().timestamp()
    token_input = f"{image_id}{random_part}{timestamp}"
    token = hashlib.sha256(token_input.encode()).hexdigest()[:16]

    #calculate expiry date
    expires_at = datetime.now() + timedelta(minutes=10)

    #load existing tokens
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as token_file:
            tokens = json.load(token_file)
    else:
        tokens = {}

    #save new token
    tokens[token] = {
        "image_id": image_id,
        "expires_at": expires_at.isoformat()
    }

    with open(TOKENS_FILE, 'w') as token_file:
        json.dump(tokens, token_file)
    
    return jsonify({
        "token": token,
        "url": f"/s/{token}",
        "expires_at": expires_at.isoformat()
    })

@app.route('/s/<token>', methods=['GET'])
def shared_page(token):
    #log tokens from file
    TOKENS_FILE = './data/tokens.json'

    if not os.path.exists(TOKENS_FILE):
        return "link invalid or expired", 404
    
    with open(TOKENS_FILE, 'r') as token_file:
        tokens = json.load(token_file)

    #check if token exists
    if token not in tokens:
        return "link invalid or expired", 404
    
    #get token data
    token_data = tokens[token]
    image_id = token_data['image_id']
    expires_at_str = token_data['expires_at']

    #check if image exists
    image_path = os.path.join(UPLOAD_DIR, image_id)
    if not os.path.exists(image_path):
        return "image not found", 404
    
    #check not expired
    expires_at = datetime.fromisoformat(expires_at_str)
    if datetime.now() > expires_at:
        #clear expired tokens
        del tokens[token]
        with open(TOKENS_FILE, 'w') as token_file:
            json.dump(tokens, token_file)
        return "this share link has expired", 410
    
    #create url for image
    image_url = f"/uploads/{image_id}"

    #get image info for display
    img = Image.open(image_path)
    analysis = {
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "size_kb": round(os.path.getsize(image_path) / 1024, 2)
    }

    #TO DO add html return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)