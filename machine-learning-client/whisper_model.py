"""This module handles the machine learning aspects using Whisper model."""
import ssl
import whisper

base_model = whisper.load_model("base")
result = base_model.transcribe("/Users/wayne/Desktop/Hikaru Takes The Juicer-UfAV4mpJn6A.wav")
print(result["text"])
