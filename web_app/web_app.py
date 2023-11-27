from flask import Flask, request, jsonify, render_template, redirect, url_for
import whisper

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        if file:
            filename = "uploaded_audio.wav"
            file.save(filename)

            # Transcribe using Whisper
            base_model = whisper.load_model("base")
            result = base_model.transcribe(filename)
            transcription = result["text"]

    return render_template('webpage.html', transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True)
