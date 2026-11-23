import wave
from pathlib import Path

import numpy as np
import sherpa_onnx
from huggingface_hub import hf_hub_download

here = Path(__file__).parent
repo = "Axiveri/Renpiper-mms-onnx-V1"
model = hf_hub_download(repo, "pcm/model.onnx")
tokens = hf_hub_download(repo, "pcm/tokens.txt")

config = sherpa_onnx.OfflineTtsConfig(
    model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=model, tokens=tokens),
        num_threads=2,
    )
)
tts = sherpa_onnx.OfflineTts(config)

lines = [
    line.strip()
    for line in (here / "sentences_pcm.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
]

for i, text in enumerate(lines, 1):
    audio = tts.generate(text)
    samples = np.clip(np.array(audio.samples, dtype=np.float32), -1, 1)
    pcm16 = (samples * 32767).astype(np.int16)
    out = f"pcm_{i}.wav"
    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(audio.sample_rate)
        w.writeframes(pcm16.tobytes())
    print(f"saved {out}: {text} ({len(samples) / audio.sample_rate:.2f}s)")
