"""This module handles the machine learning aspects using Whisper model."""
# import ssl
# import os
import whisper
from flask import Flask, request
from pymongo.mongo_client import MongoClient
from flask_cors import CORS

# MONGO_URI = "mongodb://mongodb:27017/stuyTownistas"
# client = MongoClient(MONGO_URI)
# db = client.get_database("whisper_db")

# app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    MONGO_URI = "mongodb://mongodb:27017/stuyTownistas"
    client = MongoClient(MONGO_URI)
    db = client.get_database("whisper_db")

    @app.route("/api/", methods=["POST"])
    def transcribe_audio():
        """Transcribes the audio file sent to the server."""
        # audio_blob = request.files["file"]
        # audio_id = fs.put(audio_blob, filename="uploaded_audio.wav", content_type="audio/wav")
        # return jsonify({"audio_id": str(audio_id)})
        base_model = whisper.load_model("base")
        files = request.files
        whisper_request = None 

        if "file" in files:
            file = files.get("file")
            file_content = file.read()
            whisper_request = {"mimetype": file.mimetype, "buffer": file_content}

        if not whisper_request:
            raise ValueError("No file provided for transcription.")
        result = base_model.transcribe(whisper_request)
        transcription = result["text"]
        save = {"transcription": transcription}
        db.transcriptions.insert_one(save)

        return transcription
    return app
    


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5002)
