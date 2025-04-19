from flask import Flask, request, jsonify
import subprocess
import shlex
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
# Folder to save uploaded files
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file provided.'}), 400

        file = request.files['file']

        # Ensure it's a valid file
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected.'}), 400

        # Save the file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({'status': 'success', 'message': f'File uploaded successfully to {filepath}.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
@app.route('/run/install-requirements', methods=['POST'])
def install_requirements():
    try:
        result = subprocess.run(shlex.split('pip install -r requirements.txt'), capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/run/populate-database', methods=['POST'])
def populate_database():
    try:
        result = subprocess.run(shlex.split('python populate_database.py'), capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/run/query', methods=['POST'])
def query_data():
    try:
        data = request.json
        query_text = data.get('query')
        if not query_text:
            return jsonify({'status': 'error', 'message': 'Query text is required.'}), 400

        command = f'python query_data.py "{query_text}"'
        result = subprocess.run(shlex.split(command), capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
@app.route('/run/update-prompt-template', methods=['POST'])
def update_prompt_template():
    try:
        data = request.json
        new_template = data.get('prompt_template')
        if not new_template:
            return jsonify({'status': 'error', 'message': 'prompt_template is required.'}), 400

        with open('prompt_template.txt', 'w') as f:
            f.write(new_template)

        return jsonify({'status': 'success', 'message': 'Prompt template updated successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
        
if __name__ == '__main__':
    app.run(debug=True)