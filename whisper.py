import whisper
import csv

model = whisper.load_model("medium")

options = {"language": "de"}
result = model.transcribe("./audio/audio.mp3", **options)
#result = model.transcribe(r"C:\Users\schau\PycharmProjects\Whisper\whisper\audio.mp3", **options)

#Inhalt in Variable schreiben
result_text = result["text"]
print(result_text)

# Definieren Sie den Dateinamen, unter dem Sie die CSV-Datei speichern möchten
dateiname = "./audio/audio_transcript.csv"

# Öffnen Sie die Datei im Schreibmodus und geben Sie an, dass es sich um eine CSV-Datei handelt
with open(dateiname, mode='w', newline='') as csv_datei:
    csv_schreiber = csv.writer(csv_datei)

    # Schreiben Sie den Text in die CSV-Datei
    csv_schreiber.writerow([result_text])

