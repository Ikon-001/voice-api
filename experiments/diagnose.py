import numpy as np
import torch
from transformers import VitsModel, AutoTokenizer

name = "Shinzmann/soro-tts-ibo"
tokenizer = AutoTokenizer.from_pretrained(name)
model = VitsModel.from_pretrained(name)

with open("sentences.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for i, text in enumerate(lines, 1):
    inputs = tokenizer(text, return_tensors="pt")
    n_tokens = inputs["input_ids"].shape[1]
    with torch.no_grad():
        wave = model(**inputs).waveform[0].numpy()
    seconds = len(wave) / model.config.sampling_rate
    print(f"{i}: {text!r}")
    print(f"   tokens={n_tokens} seconds={seconds:.2f} max_amp={np.abs(wave).max():.4f} has_nan={bool(np.isnan(wave).any())}")
