import io
import json
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from whisper_model import create_app
from flask_cors import CORS
from pymongo.mongo_client import MongoClient

# @app.route("/api/", methods=["POST"])

# MONGO_URI = "mongodb://mongodb:27017/stuyTownistas"
# client = MongoClient(MONGO_URI)
# db = client.get_database("whisper_db")

# app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@pytest.fixture
def client():
    
    app = create_app()  # Make sure create_app() correctly sets up your Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transcribe_audio_success(client):
    # Mock the whisper model and MongoDB
    with patch("whisper.load_model") as mock_whisper, \
         patch("whisper_model.MongoClient") as mock_mongo:

        # Set up the mock return values
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "transcribed text"}
        mock_whisper.return_value = mock_model
        mock_mongo.return_value.get_database.return_value.transcriptions.insert_one = MagicMock()

        # Create a mock file
        data = {
            "file": (io.BytesIO(b"audio data"), "test.wav")
        }

        # Send a POST request to the API
        response = client.post("/api/", content_type='multipart/form-data', data=data)

        # Check that the response is as expected
        assert response.status_code == 200
        assert response.data.decode() == "transcribed text"

def test_transcribe_audio_no_file(client):
    with patch("whisper_model.MongoClient") as mock_mongo:
        # Test for the case when no file is provided in the request
        response = client.post("/api/", content_type='multipart/form-data', data={})
        assert response.status_code == 400  # Assuming you change the error handling to return a 400 Bad Request
