"""
Утилиты для обработки текста и данных
"""
from .text_processor import (
    normalize_numbers,
    normalize_letters,
    clean_text_for_speech,
    extract_topic
)

__all__ = [
    'normalize_numbers',
    'normalize_letters',
    'clean_text_for_speech',
    'extract_topic'
]
