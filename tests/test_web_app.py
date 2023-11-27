import pytest
import os
from flask import Flask
from werkzeug.datastructures import FileStorage
# from web_app.py import app
from web_app.web_app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Transcription' in response.data

def test_index_post_no_file(client):
    response = client.post('/')
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_index_post_no_selected_file(client):
    data = {'file': (FileStorage(stream=b''), '')}
    response = client.post('/', data=data)
    assert response.status_code == 400
    assert b'No selected file' in response.data

def test_index_post_with_file(client):
    audio_file_path = os.path.join(os.path.dirname(__file__), 'uploaded_audio.wav')
    data = {'file': (open(audio_file_path, 'rb'), 'uploaded_audio.wav')}
    response = client.post('/', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Transcription' in response.data
