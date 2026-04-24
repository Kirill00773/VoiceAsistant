"""
Модуль распознавания речи (Speech-to-Text)
"""
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import numpy as np

MODEL_SIZE = "base"
SAMPLE_RATE = 16000
AUDIO_FILE = "input.wav"

# Инициализация модели Whisper
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def record_audio(filename=AUDIO_FILE, duration=5):
    """
    Записывает аудио с микрофона

    Args:
        filename: путь для сохранения аудио
        duration: длительность записи в секундах
    """
    print("🎤 Говорите...")

    try:
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        # Нормализация аудио
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))

        write(filename, SAMPLE_RATE, audio)
        print("✓ Запись завершена")

    except Exception as e:
        print(f"❌ Ошибка записи: {e}")
        raise


def transcribe_audio(filename=AUDIO_FILE):
    """
    Распознаёт речь из аудиофайла

    Args:
        filename: путь к аудиофайлу

    Returns:
        str: распознанный текст
    """
    try:
        segments, info = model.transcribe(
            filename,
            language="ru",
            vad_filter=True,  # фильтр тишины
            word_timestamps=True  # для лучшего распознавания цифр
        )

        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())

        result = " ".join(text_parts)
        return result if result else ""

    except Exception as e:
        print(f"❌ Ошибка распознавания: {e}")
        return ""