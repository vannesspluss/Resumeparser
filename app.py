import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from parser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))

UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_PATH, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Resume Parser API is live."})

@app.route("/process", methods=["POST"])
def ats():
    try:
        doc = request.files['pdf_doc']
        doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
        doc.save(doc_path)

        resume_text = _read_file_from_path(doc_path)
        parsed_data = ats_extractor(resume_text)

        return jsonify(json.loads(parsed_data))

    except Exception as e:
        return jsonify({"error": "Failed to parse resume", "details": str(e)}), 500

def _read_file_from_path(path):
    reader = PdfReader(path)
    data = ""
    for page in reader.pages:
        data += page.extract_text()
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
