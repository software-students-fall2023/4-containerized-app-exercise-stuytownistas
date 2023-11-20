import ssl
import whisper

# Disable SSL verification - NOT recommended for anything else! Just a temporary workaround to a bug.
ssl._create_default_https_context = ssl._create_unverified_context

base_model = whisper.load_model("base")
result = base_model.transcribe("/Users/wayne/Music/GarageBand/lofi thing.band/Media/Audio Files/Hikaru Nakamura - Stream Highlights-v4a-RY2r7og.wav")
print(result["text"])