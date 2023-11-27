import os
import tempfile
import pytest
from flask.testing import FlaskClient
from machine_learning_client.whisper_model import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_index_post_no_file(client: FlaskClient):
    response = client.post('/')
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_index_post_no_selected_file(client: FlaskClient):
    response = client.post('/', data=dict(file='', method='POST'))
    assert response.status_code == 400
    assert b'No selected file' in response.data

def test_index_post_with_file(client: FlaskClient):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        response = client.post('/', data={'file': (temp_file, 'test.wav')})
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert b'Transcription: ' in response.data

    os.unlink(temp_file.name)
