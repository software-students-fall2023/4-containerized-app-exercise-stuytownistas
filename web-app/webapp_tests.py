import os
import io
import tempfile
import pytest
from flask import Flask, request, jsonify
import whisper
from web_app import app, fs  # Import your Flask app and GridFS instance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """
    Test the index route.
    """
    response = client.get("/")
    assert response.status_code == 200  

def test_transcribe_audio(client, monkeypatch):
    # Mocking whisper.load_model to avoid actual transcription in the test
    def mock_load_model(*args, **kwargs):
        class MockModel:
            def transcribe(self, audio_path):
                return {"text": "Mocked transcription"}

        return MockModel()

    monkeypatch.setattr('whisper.load_model', mock_load_model)

    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_audio_path = f.name
        f.write(b'Test audio content')

    # Mocking GridFS get method to return some data
    class MockGridFSFile:
        def read(self):
            return b'Test audio content'

    def mock_gridfs_get(audio_id):
        return MockGridFSFile()

    monkeypatch.setattr(fs, 'get', mock_gridfs_get)

    # Make a request to the route
    response = client.get('/transcribe/123')

    # Assert the response
    assert response.status_code == 200
    data = response.get_json()
    assert 'transcription' in data
    assert data['transcription'] == 'Mocked transcription'

    # Clean up the temporary audio file
    os.remove(temp_audio_path)
