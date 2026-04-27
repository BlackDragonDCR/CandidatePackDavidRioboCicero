from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = './data/uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)