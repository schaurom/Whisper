import whisper
import pandas as pd

model = whisper.load_model("medium")

options = {"language": "de"}
result = model.transcribe("./audio/audio.mp3", **options)
#result = model.transcribe(r"C:\Users\schau\PycharmProjects\Whisper\whisper\audio.mp3", **options)
print(result["text"])

df = pd.DataFrame(result["text"])
df.to_csv("./audio/audio_transcript.csv", index=False)
