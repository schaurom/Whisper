import os
from flask import Flask, request, render_template, send_file
import tempfile
import torch
#from transformers import WhisperForConditionalGeneration, WhisperTokenizer
import whisper

app = Flask(__name__)

# Laden Sie das Whisper-Modell und den Tokenizer
#model = WhisperForConditionalGeneration.from_pretrained("facebook/whisper-large")
#tokenizer = WhisperTokenizer.from_pretrained("facebook/whisper-large")
model = whisper.load_model("medium")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Überprüfen, ob eine Datei hochgeladen wurde
        if 'file' not in request.files:
            return render_template('index.html', error='Keine Datei ausgewählt')

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='Keine Datei ausgewählt')

        # Speichern Sie die hochgeladene Datei vorübergehend
        audio_file_path = tempfile.mktemp(suffix=".wav")
        file.save(audio_file_path)

        # Transkribieren Sie die Audiodatei
        options = {"language": "de"}
        transcription_text = model.transcribe(audio_file_path, **options)

        # Text in eine temporäre Datei schreiben
        output_file_path = tempfile.mktemp(suffix=".txt")
        with open(output_file_path, 'w') as output_file:
            output_file.write(transcription_text)

        # Datei zum Download bereitstellen
        response = send_file(output_file_path, as_attachment=True, download_name='transcription.txt')

        # Hochgeladene Audiodatei und temporäre Textdatei löschen
        os.remove(audio_file_path)
        os.remove(output_file_path)

        return response

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
