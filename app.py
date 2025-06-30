# app.py
import os
import sys
from flask import Flask, request, jsonify
from pypdf import PdfReader 
from flask_cors import CORS
from parser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))
UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_PATH, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Resume Parser API is running."})

@app.route("/process", methods=["POST"])
def ats():
    if 'pdf_doc' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    doc = request.files['pdf_doc']
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    doc.save(doc_path)

    data = _read_file_from_path(doc_path)
    extracted = ats_extractor(data)
    
    try:
        # Convert string JSON from OpenAI response to Python dict
        return jsonify(json.loads(extracted))
    except Exception as e:
        return jsonify({"error": "Invalid response format", "details": str(e)}), 500

def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""
    for page in reader.pages:
        data += page.extract_text() or ""
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
