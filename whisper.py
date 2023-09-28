import whisper
import numpy as np

model = whisper.load_model("medium")

options = {"language": "de"}
result = model.transcribe("./audio/audio.mp3", **options)
#result = model.transcribe(r"C:\Users\schau\PycharmProjects\Whisper\whisper\audio.mp3", **options)
print(result["text"])

np.savetxt("./audio/audio_transcript.csv", result["text"])
#