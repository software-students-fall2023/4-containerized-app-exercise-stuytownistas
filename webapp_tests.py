import os
import io
import tempfile
import pytest
from flask import Flask, request, jsonify
from app import app, fs  # Import your Flask app and GridFS instance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload(client):
    data = {'file': (io.BytesIO(b"dummy content"), 'test.wav')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'audio_id' in response.json

def test_get_audio(client):
    # Assuming you have an audio file already uploaded for testing
    audio_data = b"dummy audio content"
    audio_id = fs.put(audio_data, filename='test_audio.wav', content_type='audio/wav')

    response = client.get(f'/get_audio/{str(audio_id)}')

    assert response.status_code == 200
    assert response.mimetype == 'audio/wav'
    assert response.headers['Content-Disposition'] == 'attachment; filename=uploaded_audio.wav'
    assert response.data == audio_data

def test_transcribe_audio(client):
    # Assuming you have an audio file already uploaded for testing
    audio_data = b"dummy audio content"
    audio_id = fs.put(audio_data, filename='test_audio.wav', content_type='audio/wav')

    response = client.get(f'/transcribe/{str(audio_id)}')

    assert response.status_code == 200
    assert 'transcription' in response.json

def test_index(client):
    # Assuming you have an audio file already uploaded for testing
    audio_data = b"dummy audio content"
    audio_id = fs.put(audio_data, filename='test_audio.wav', content_type='audio/wav')

    data = {'audio_id': str(audio_id)}
    response = client.post('/', data=data)

    assert response.status_code == 200
    assert 'Error processing the file' not in response.get_data(as_text=True)
