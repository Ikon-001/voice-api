from abc import ABC, abstractmethod

import numpy as np


class SpeechEngine(ABC):
    """Turns text into audio. One subclass per model."""

    name: str = ""
    languages: tuple[str, ...] = ()

    @abstractmethod
    def synthesize(self, text: str, speed: float = 1.0) -> tuple[np.ndarray, int]:
        """Return (float32 samples between -1 and 1, sample rate in Hz)."""


class TranscriptionEngine(ABC):
    """PLANNED, not implemented yet. Turns audio into text.

    Candidate model: a small Nigerian Pidgin Moonshine fine-tune (untested).
    """

    name: str = ""
    languages: tuple[str, ...] = ()

    @abstractmethod
    def transcribe(self, audio_bytes: bytes, language: str) -> str:
        """Return the transcript."""