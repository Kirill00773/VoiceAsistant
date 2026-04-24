"""
Голосовой ассистент с RAG (Retrieval-Augmented Generation)
Использует распознавание речи, поиск по базе знаний и синтез речи
"""
import sys
from voice.stt import record_audio, transcribe_audio
from voice.tts import speak
from rag.qa import retrieve_context, generate_answer
from utils.text_processor import extract_topic


def print_separator():
    """Печатает разделитель для улучшения читаемости"""
    print("\n" + "=" * 60 + "\n")


def display_context(results):
    """
    Отображает найденный контекст из базы знаний

    Args:
        results: список документов с релевантной информацией
    """
    if not results:
        print("⚠️ Контекст не найден")
        return

    print(f"📚 Найдено фрагментов: {len(results)}")
    for i, doc in enumerate(results, start=1):
        print(f"\n  [{i}] {doc.page_content[:100]}...")


def main():
    """Основной цикл работы голосового ассистента"""
    print_separator()
    print("🤖 Голосовой ассистент лаборатории запущен!")
    print("\nКоманды:")
    print("  - Скажите 'выход' или 'exit' для завершения")
    print("  - Задавайте вопросы о лаборатории")
    print_separator()

    while True:
        try:
            # Запись аудио
            record_audio()

            # Распознавание речи
            query = transcribe_audio()

            if not query:
                print("⚠️ Не удалось распознать речь. Попробуйте ещё раз.\n")
                continue

            print(f"\n💬 Вы сказали: {query}")

            # Проверка команды выхода
            if query.lower().strip() in ["выход", "exit", "стоп", "stop"]:
                print("\n👋 Завершаю работу. До встречи!")
                break

            # Определение темы вопроса
            topic = extract_topic(query)
            print(f"🎯 Тема: {topic}")

            # Поиск релевантного контекста
            context, results = retrieve_context(query)
            display_context(results)

            # Генерация ответа
            print("\n🤔 Думаю...")
            answer = generate_answer(query, context)

            print(f"\n🤖 Ассистент: {answer}")

            # Озвучивание ответа
            speak(answer)

            print_separator()

        except KeyboardInterrupt:
            print("\n\n⚠️ Прервано пользователем")
            break

        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            print("Попробуйте ещё раз\n")
            continue


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)