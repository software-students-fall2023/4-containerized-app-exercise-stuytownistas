import os
import pytest
from unittest.mock import patch, Mock
import whisper

base_model = whisper.load_model("base")

def test_transcribe_success():
    # Mock the whisper.load_model function
    with patch('whisper.load_model', return_value=Mock(transcribe=Mock(return_value={"text": "Test transcription"}))):
        # Call the transcribe method with a test file
        result = base_model.transcribe("web_app/uploaded_audio.wav")
    
    # Assert that the result matches the expected output
    assert result == {"text": "Test transcription"}

def test_transcribe_failure():
    with patch('whisper.load_model', side_effect=Exception("Model loading failed")):
        with pytest.raises(Exception, match="Model loading failed"):
            base_model.transcribe("uploaded_audio.wav")

def test_main_function():
    with patch('whisper.load_model', return_value=Mock(transcribe=Mock(return_value={"text": "Test transcription"}))):
        with patch('builtins.print') as mock_print:
            with patch('ssl._create_unverified_context', return_value=ssl.SSLContext()):
                from whisper_module import main_function
                main_function("/path/to/audio/file.wav")
                mock_print.assert_called_with("Test transcription")