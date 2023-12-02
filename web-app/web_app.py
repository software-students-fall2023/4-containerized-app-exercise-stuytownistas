from flask import Flask, request, jsonify, render_template, send_file
import whisper
# from gridfs import GridFS
import io
from pymongo import MongoClient
import subprocess
from bson import Binary
import os
from datetime import datetime

# MongoDB URI and Connection
mongo_uri = "mongodb://mongodb:27017/stuyTownistas"
client = MongoClient(mongo_uri)
db = client["audio"]
collection = db["audio-collection"]
# db = client.get_database('whisper_db')
# fs = GridFS(db)
print(client.list_database_names())

app = Flask(__name__)

def convert_to_wav(input_data):
    """
    Converts an audio file to WAV format using FFmpeg.

    Parameters:
    input_data (bytes): The input audio data.
    input_format (str): The format of the input audio data.

    Returns:
    bytes: The converted audio data in WAV format.
    """
    with open("temp_input_file", "wb") as temp_input:
        temp_input.write(input_data)

    output_file = "temp_output_file.wav"
    command = [
        "ffmpeg",
        "-i",
        "temp_input_file",
        "-ar",
        "44100",
        "-ac",
        "2",
        output_file,
    ]
    try:
        subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError as e:
        print("An error occurred while converting the file: ", e)
        return None

    with open(output_file, "rb") as wav_output:
        wav_data = wav_output.read()

    os.remove("temp_input_file")
    os.remove(output_file)
    return wav_data



@app.route('/')
def index():
    return render_template('webpage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file:
        file_data = file.read()
        wav_file = convert_to_wav(file_data)
        filename = "test_audio.wav"
        file.save(filename)

        audio_file = {
            "name": file.filename,
            "audio_data": Binary(wav_file),
            "recorded_date": datetime.utcnow().strftime("%B %d %H:%M:%S"),
        }
    
        # Store file as binary. (This step isn't working right now)
        collection.insert_one(audio_file)

        # Transcribe using Whisper. (This should be in ml_client file)
        base_model = whisper.load_model("base")
        result = base_model.transcribe(file_data)
        transcription = result["text"]

        print("Transcription:", transcription)

        return jsonify(transcription=transcription)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
