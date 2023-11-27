import os
import pytest
from unittest.mock import patch, Mock
from whisper_module import base_model

def test_transcribe_success():
    with patch('whisper.load_model', return_value=Mock(transcribe=Mock(return_value={"text": "Test transcription"}))):
        result = base_model.transcribe("uploaded_audio.wav")
    
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