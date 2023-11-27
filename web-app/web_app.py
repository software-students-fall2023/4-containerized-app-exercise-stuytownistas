from flask import Flask, request, jsonify, render_template, send_file
import whisper
from gridfs import GridFS
import io
from pymongo import MongoClient

# MongoDB URI and Connection
mongo_uri = "mongodb://mongodb:27017/stuyTownistas"
client = MongoClient(mongo_uri)
db = client.get_database('whisper_db')
fs = GridFS(db)

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
        audio_id = request.form['audio_id']
        try:
            audio_data = fs.get(audio_id)
            with open("uploaded_audio.wav", "wb") as f:
                f.write(audio_data.read())

            # Transcribe using Whisper
            base_model = whisper.load_model("base")
            result = base_model.transcribe("uploaded_audio.wav")
            transcription = result["text"]

        except Exception as e:
            print(e)
            return 'Error processing the file', 500

    return render_template('webpage.html', transcription=transcription)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
