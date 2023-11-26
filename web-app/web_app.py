from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import whisper
from gridfs import GridFS
import io

from pymongo import MongoClient

# Connect to the MongoDB instance running on the host machine
# client = MongoClient('localhost', 27017)
mongo_uri = "mongodb://mongodb:27017/stuyTownistas"
client = MongoClient(mongo_uri)
db = client.get_database()

# client = MongoClient()
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Access the database (replace 'your_database' with the actual name)
db = client['whisper_db']
fs = GridFS(db)
audio_collection = db.audio_collection


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    audio_blob = request.files['file']
    audio_id = fs.put(audio_blob, filename='audio.wav', content_type='audio/wav')
    return jsonify({'audio_id': str(audio_id)})

@app.route('/get_audio/<audio_id>')
def get_audio(audio_id):
    audio_data = fs.get(audio_id)
    return send_file(io.BytesIO(audio_data.read()), mimetype='audio/wav', as_attachment=True, download_name='audio.wav')

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        if file:
            filename = "uploaded_audio.wav"
            file.save(filename)

            # Transcribe using Whisper
            base_model = whisper.load_model("base")
            result = base_model.transcribe(filename)
            transcription = result["text"]

    return render_template('webpage.html', transcription=transcription)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
