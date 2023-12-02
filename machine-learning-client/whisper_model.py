"""This module handles the machine learning aspects using Whisper model."""
import ssl
import whisper
import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI"))
database = client[os.getenv("MONGO_DATABASE")]
collection = database[os.getenv("MONGO_COLLECTION")]

base_model = whisper.load_model("base")
result = base_model.transcribe("/Users/wayne/Desktop/Hikaru Takes The Juicer-UfAV4mpJn6A.wav")
print(result["text"])
