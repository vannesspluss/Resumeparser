import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
import json
from parser import ats_extractor
from flask_cors import CORS


sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_PATH, exist_ok=True)

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")
    data = _read_file_from_path(doc_path)
    data = ats_extractor(data)

    return render_template('index.html', data = json.loads(data))
 
def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
