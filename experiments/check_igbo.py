import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer

name = "Shinzmann/soro-tts-ibo"
tokenizer = AutoTokenizer.from_pretrained(name)
model = VitsModel.from_pretrained(name)

with open("sentences.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for i, text in enumerate(lines, 1):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        wave = model(**inputs).waveform[0].numpy()
    out = f"igbo_{i}.wav"
    scipy.io.wavfile.write(out, model.config.sampling_rate, wave)
    print(f"saved {out}: {text}")
