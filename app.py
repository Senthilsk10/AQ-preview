from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import importlib.util
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import json

UPLOAD_FOLDER = 'static/uploaded'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded', 'path': file_path})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/preview-auto-question', methods=['POST'])
def preview_auto_question():
    try:
        data = request.get_json()
        uploaded_file_path = data.get('path')
        question_type = int(data.get('question_type', 1))
        question_level = int(data.get('question_level', 1))

        if not os.path.exists(uploaded_file_path):
            return jsonify({'error': 'Uploaded file not found'}), 400

        with open(uploaded_file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        with NamedTemporaryFile(mode='w', suffix='.py', encoding='utf-8', delete=False) as temp_f:
            temp_f.write(code)
            temp_file_path = temp_f.name

        try:
            spec = importlib.util.spec_from_file_location("question_module", temp_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'generate_question'):
                result = module.generate_question(question_type, question_level)
                print(result)
                parsed = json.loads(result)
                print('parsed',parsed)
                return jsonify({
                    'output': {
                        'question': parsed['question'],
                        'options': parsed['options'],
                        'correctAnswer': parsed['correctAnswer']
                    }
                })
            else:
                return jsonify({'error': 'generate_question() not found'}), 400
        finally:
            os.unlink(temp_file_path)

    except Exception as e:
        print(e)    
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
