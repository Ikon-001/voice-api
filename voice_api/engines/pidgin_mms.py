import threading

import numpy as np
import sherpa_onnx
from huggingface_hub import hf_hub_download

from .base import SpeechEngine

REPO = "Axiveri/Renpiper-mms-onnx-V1"


class PidginMmsEngine(SpeechEngine):
    name = "mms-pcm"
    languages = ("pcm",)

    def __init__(self):
        self._tts = None
        self._lock = threading.Lock()

    def _load(self):
        if self._tts is None:
            model = hf_hub_download(REPO, "pcm/model.onnx")
            tokens = hf_hub_download(REPO, "pcm/tokens.txt")
            config = sherpa_onnx.OfflineTtsConfig(
                model=sherpa_onnx.OfflineTtsModelConfig(
                    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=model, tokens=tokens),
                    num_threads=2,
                )
            )
            self._tts = sherpa_onnx.OfflineTts(config)

    def synthesize(self, text, speed=1.0):
        with self._lock:
            self._load()
            audio = self._tts.generate(text, sid=0, speed=speed)
        return np.array(audio.samples, dtype=np.float32), audio.sample_rate
