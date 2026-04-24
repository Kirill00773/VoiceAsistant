"""
Модули для работы с голосом: распознавание (STT) и синтез (TTS)
"""
from .stt import record_audio, transcribe_audio
from .tts import speak

__all__ = ['record_audio', 'transcribe_audio', 'speak']
