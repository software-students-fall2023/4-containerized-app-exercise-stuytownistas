from flask import Flask, request, jsonify, render_template, redirect, url_for
import whisper

from pymongo import MongoClient

# Connect to the MongoDB instance running on the host machine
client = MongoClient("mongodb://localhost:27117/")

client = MongoClient()
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Access the database (replace 'your_database' with the actual name)
db = client['whisper_db']
audio_collection = db.audio_collection


app = Flask(__name__)

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
    app.run(debug=True)
