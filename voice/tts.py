"""
Модуль синтеза речи (Text-to-Speech)
"""
import torch
import sounddevice as sd
import sys
import os

# Добавляем путь к utils для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_processor import clean_text_for_speech

# Загружаем модель Silero TTS
model, _ = torch.hub.load(
    'snakers4/silero-models',
    'silero_tts',
    language='ru',
    speaker='v3_1_ru',
    trust_repo=True
)

SAMPLE_RATE = 48000
SPEAKER = 'kseniya'


def speak(text: str):
    """
    Озвучивает текст с помощью Silero TTS

    Args:
        text: текст для озвучивания
    """
    if not text or not text.strip():
        print("⚠️ Пустой текст для озвучивания")
        return

    try:
        # Нормализуем текст для правильного озвучивания цифр и букв
        normalized_text = clean_text_for_speech(text)

        print(f"🔊 Озвучиваю: {normalized_text[:100]}...")

        # Генерируем аудио
        audio = model.apply_tts(
            text=normalized_text,
            speaker=SPEAKER,
            sample_rate=SAMPLE_RATE
        )

        # Воспроизводим
        sd.play(audio, SAMPLE_RATE)
        sd.wait()

    except Exception as e:
        print(f"❌ Ошибка озвучивания: {e}")