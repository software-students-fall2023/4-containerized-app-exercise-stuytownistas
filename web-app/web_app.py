'''Web app for Project 4'''
import io
import traceback
import tempfile
import os
from flask import Flask, request, jsonify, render_template, send_file, flash, redirect
import whisper
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
# import requests
from werkzeug.utils import secure_filename


# MongoDB URI and Connection
MONGO_URI = "mongodb://mongodb:27017/stuyTownistas"
client = MongoClient(MONGO_URI)
db = client.get_database('whisper_db')
fs = GridFS(db)

app = Flask(__name__)

# @app.route('/upload', methods=['POST'])
# def upload():
#     audio_blob = request.files['file']
#     audio_id = fs.put(audio_blob, filename='uploaded_audio.wav', content_type='audio/wav')
#     return jsonify({'audio_id': str(audio_id)})
uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)  # Ensure the directory exists
app.config['UPLOAD_FOLDER'] = uploads_dir  # Corrected from 'uploads' to 'UPLOAD_FOLDER'

@app.route('/upload', methods=['POST'])
def upload():
    '''Uploads the audio file to the server.'''
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)

    if file:  # if file is not empty
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  #  key to 'UPLOAD_FOLDER'
        file.save(file_path)  # Save file to uploads directory

        # Assuming you want to save the file to GridFS as well
        with open(file_path, 'rb') as f:
            audio_id = fs.put(f, filename=filename, content_type='audio/wav')
        # If you need to send the file to another API
        # (Uncomment and adjust the following block if needed)
        # with open(file_path, 'rb') as f:
        #     res = requests.post(
        #         "http://localhost:5002/api",
        #         data=f.read(),
        #         headers={"Content-Type": "audio/wav"},  # Assuming the file is a WAV file
        #         timeout=20
        #     )
        # if res.status_code == 200:
        #     return res.json()  # If the other API provides a JSON response
        # else:
        #     return jsonify({'error':
        # 'Failed to process the file'}), res.status_code  # Handle non-200 responses
        # Return the audio_id in the response
        return jsonify({'audio_id': str(audio_id)})
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/get_audio/<audio_id>')
def get_audio(audio_id):
    '''Retrieves the audio file from the server.'''
    try:
        audio_data = fs.get(ObjectId(audio_id))
        return send_file(io.BytesIO(audio_data.read()), mimetype='audio/wav',
                         as_attachment=True, download_name='uploaded_audio.wav')
    except FileNotFoundError as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# @app.route('/transcribe/<audio_id>')
# def transcribe_audio(audio_id):
#     try:
#         audio_data = fs.get(ObjectId(audio_id))
#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
#             temp_audio_path = f.name
#             f.write(audio_data.read())

#         # Transcribe using Whisper
#         base_model = whisper.load_model("base")
#         result = base_model.transcribe(temp_audio_path)
#         transcription = result["text"]
#         os.remove(temp_audio_path)  # Clean up the temp file
#         return jsonify({'transcription': transcription})
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

@app.route('/transcribe/<audio_id>')
def transcribe_audio(audio_id):
    '''Transcribes the audio file sent to the server.'''
    temp_audio_path = None
    try:
        # Retrieve the audio file from GridFS
        audio_data = fs.get(ObjectId(audio_id))

        # Create a temporary file to store the audio for transcription
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_audio_path = f.name
            f.write(audio_data.read())

        # Transcribe using Whisper
        base_model = whisper.load_model("base")
        result = base_model.transcribe(temp_audio_path)
        transcription = result["text"]

        return jsonify({'transcription': transcription})
    except FileNotFoundError as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temp file if it was created
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    '''Renders the webpage.'''
    transcription = ''
    if request.method == 'POST':
        audio_id = request.form['audio_id']
        try:
            audio_data = fs.get(audio_id)
            with open("uploaded_audio.wav", "wb") as f:
                f.write(audio_data.read())

            # Transcribe using Whisper
            base_model = whisper.load_model("base")
            result = base_model.transcribe("uploaded_audio.wav")
            transcription = result["text"]

        except FileNotFoundError as e:
            print(e)
            return 'Error processing the file', 500

    return render_template('webpage.html', transcription=transcription)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
