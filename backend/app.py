from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = './data/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "no image"}), 400
    return jsonify({"message": "archivo recibido"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)