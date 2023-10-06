import os
from flask import Flask, request, render_template, send_file, session
import tempfile
import whisper
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

app = Flask(__name__)
# Setzen Sie den geheimen Schlüssel für die Sitzung aus der Umgebungsvariablen-Datei .env
app.secret_key = os.getenv('SECRET_KEY')
#html_template = 'index.html'
html_template = 'index_simple.html'

# Laden Sie das Whisper-Modell
model = whisper.load_model("medium", download_root='.\models')

@app.route('/')
def index():
    print('Seite geladen')
    #render_template(html_template, status='Seite geladen')
    return render_template(html_template, status='Seite geladen')

@app.route('/transcribe', methods=['POST', 'GET'])
def transcribe():
        # Überprüfen, ob eine Datei hochgeladen wurde
        if 'file' not in request.files:
            return render_template(html_template, error='Keine Datei ausgewählt')

        file = request.files['file']
        if file.filename == '':
            return render_template(html_template, error='Keine Datei ausgewählt')

        # Speichern Sie die hochgeladene Datei vorübergehend
        audio_file_path = tempfile.mktemp(suffix=".mp3")
        file.save(audio_file_path)
        print('Datei hochgeladen und gespeichert unter: ' + audio_file_path)
        render_template(html_template, status='Datei hochgeladen und gespeichert unter: ' + audio_file_path)

        # Transkribieren Sie die Audiodatei
        render_template(html_template, status='Transkription Start')
        options = {"language": "de"}
        response = model.transcribe(audio_file_path, **options)
        #Statusmeldung ausgeben
        render_template(html_template, status='Transkription abgeschlossen')

        # Extrahieren Sie die Transkription aus der Antwort
        transcription_text = response.get('text')

        if transcription_text:
            # Text in eine temporäre Datei schreiben
            output_file_path = tempfile.mktemp(suffix=".txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(transcription_text)

            print(output_file_path)
            render_template(html_template, status='Text in Datei gespeichert unter: ' + output_file_path)

            # Hochgeladene Audiodatei löschen (temporäre Textdatei nicht löschen, bis der Benutzer sie heruntergeladen hat)
            os.remove(audio_file_path)
            render_template(html_template, status='Audiodatei gelöscht: ' + audio_file_path)

            # Dateipfad zur temporären Textdatei für den Download speichern
            session['output_file_path'] = output_file_path

            return render_template(html_template, success='Transkription erfolgreich! Klicken Sie auf den Download-Button, um die Transkription herunterzuladen.')

        else:
            # Wenn keine Transkription vorhanden ist, geben Sie einen Warnhinweis zurück
            return render_template(html_template, warning='Transkription erfolgreich, aber es gab Warnungen oder Hinweise während des Prozesses')

@app.route('/download')
def download():
    # Dateipfad zur temporären Textdatei aus der Sitzung abrufen
    output_file_path = session.pop('output_file_path', None)

    if output_file_path:
        try:
            # Transkriptionsdatei zum Download bereitstellen
            response = send_file(output_file_path, as_attachment=True, download_name='transcription.txt')
        finally:
            # Datei nach dem Download löschen, egal ob der Download erfolgreich war oder nicht
            # os.remove(output_file_path)
            print()
        return response

    # Wenn kein Dateipfad vorhanden ist, zeigen Sie eine Fehlermeldung an
    return render_template(html_template, error='Transkription nicht verfügbar.')


if __name__ == '__main__':
    app.run(debug=True)
