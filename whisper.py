import whisper
import csv
from docx import Document

model = whisper.load_model("medium")

options = {"language": "de"}
result = model.transcribe("./audio/audio.mp3", **options)
#result = model.transcribe(r"C:\Users\schau\PycharmProjects\Whisper\whisper\audio.mp3", **options)

#Inhalt in Variable schreiben
result_text = result["text"]
print(result_text)

#----------------------------------------------------------------------------------------------------------------
# CSV
# Definieren Sie den Dateinamen, unter dem Sie die CSV-Datei speichern möchten
dateiname = "./audio/audio_transcript.csv"

# Öffne die Datei im Schreibmodus
# mode='w' --> Datei wird überschrieben
# mode='a' --> append --> neue Daten werden in der bestehenden Datei unten drangehängt
with open(dateiname, mode='w', newline='') as csv_datei:
    csv_schreiber = csv.writer(csv_datei)
    # Text in CSV Datei schreiben
    csv_schreiber.writerow([result_text])
#----------------------------------------------------------------------------------------------------------------
# Word
dateiname = "./audio/audio_transcript.docx"

# erstelle ein neues Word Dokument
dokument = Document()
# Fügen Sie den Text in das Dokument ein
dokument.add_paragraph(result_text)
# Speichern Sie das Dokument in einer Datei
dokument.save(dateiname)