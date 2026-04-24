"""
Утилиты для обработки текста: нормализация цифр, букв и специальных символов
"""
import re


def normalize_numbers(text: str) -> str:
    """
    Преобразует цифры в текстовое представление для лучшего озвучивания
    """
    number_map = {
        '0': 'ноль', '1': 'один', '2': 'два', '3': 'три', '4': 'четыре',
        '5': 'пять', '6': 'шесть', '7': 'семь', '8': 'восемь', '9': 'девять'
    }

    # Заменяем отдельные цифры
    for digit, word in number_map.items():
        text = re.sub(rf'\b{digit}\b', word, text)

    # Обрабатываем многозначные числа
    def replace_number(match):
        num = int(match.group())
        if num < 10:
            return number_map[str(num)]
        elif num < 20:
            teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать',
                    'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
            return teens[num - 10]
        elif num < 100:
            tens = ['', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят',
                   'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
            ones = num % 10
            return f"{tens[num // 10]} {number_map[str(ones)]}" if ones else tens[num // 10]
        else:
            return str(num)

    text = re.sub(r'\b\d+\b', replace_number, text)
    return text


def normalize_letters(text: str) -> str:
    """
    Функция очищена от автоматического добавления слова "буква",
    так как это приводило к ошибкам в произношении.
    """
    return text


def clean_text_for_speech(text: str) -> str:
    """
    Очищает и нормализует текст для озвучивания
    """
    # Убираем лишние пробелы
    text = re.sub(r'\s+', ' ', text).strip()

    # Нормализуем цифры и буквы
    text = normalize_numbers(text)
    text = normalize_letters(text)

    return text


def extract_topic(query: str) -> str:
    """
    Извлекает основную тему из вопроса пользователя
    """
    query_lower = query.lower()

    # Ключевые слова для определения темы
    topics = {
        'оборудование': ['оборудование', 'прибор', 'микроскоп', 'центрифуга', 'спектрометр'],
        'процедуры': ['процедура', 'как', 'инструкция', 'метод', 'протокол'],
        'исследования': ['исследование', 'эксперимент', 'анализ', 'тест', 'проект'],
        'безопасность': ['безопасность', 'правила', 'защита', 'опасность'],
    }

    for topic, keywords in topics.items():
        if any(keyword in query_lower for keyword in keywords):
            return topic

    return 'общее'