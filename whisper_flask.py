import os
from flask import Flask, request, render_template, send_file
import tempfile
import whisper
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

app = Flask(__name__)
# Setzen Sie den geheimen Schlüssel für die Sitzung aus der Umgebungsvariablen-Datei .env
app.secret_key = os.getenv('SECRET_KEY')

# Laden Sie das Whisper-Modell
model = whisper.load_model("medium")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
        # Überprüfen, ob eine Datei hochgeladen wurde
        if 'file' not in request.files:
            return render_template('index.html', error='Keine Datei ausgewählt')

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='Keine Datei ausgewählt')

        # Speichern Sie die hochgeladene Datei vorübergehend
        audio_file_path = tempfile.mktemp(suffix=".mp3")
        file.save(audio_file_path)

        # Transkribieren Sie die Audiodatei
        options = {"language": "de"}
        response = model.transcribe(audio_file_path, **options)

        # Extrahieren Sie die Transkription aus der Antwort
        transcription_text = response.get("transcription")

        if transcription_text:
            # Text in eine temporäre Datei schreiben
            output_file_path = tempfile.mktemp(suffix=".txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(transcription_text)

            # Hochgeladene Audiodatei löschen (temporäre Textdatei nicht löschen, bis der Benutzer sie heruntergeladen hat)
            os.remove(audio_file_path)

            # Dateipfad zur temporären Textdatei für den Download speichern
            session['output_file_path'] = output_file_path

            return render_template('index.html',
                                   success='Transkription erfolgreich! Klicken Sie auf den Download-Button, um die Transkription herunterzuladen.')

        else:
            # Wenn keine Transkription vorhanden ist, geben Sie einen Warnhinweis zurück
            return render_template('index.html',
                                   warning='Transkription erfolgreich, aber es gab Warnungen oder Hinweise während des Prozesses')

@app.route('/download')
def download():
    # Dateipfad zur temporären Textdatei aus der Sitzung abrufen
    output_file_path = session.pop('output_file_path', None)

    if output_file_path:
        # Transkriptionsdatei zum Download bereitstellen
        return send_file(output_file_path, as_attachment=True, download_name='transcription.txt')

    # Wenn kein Dateipfad vorhanden ist, zeigen Sie eine Fehlermeldung an
    return render_template('index.html', error='Transkription nicht verfügbar.')

if __name__ == '__main__':
    app.run(debug=True)
