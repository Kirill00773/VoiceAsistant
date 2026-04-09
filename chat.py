from rag.qa import retrieve_context, generate_answer


def main():
    print("Локальный ассистент запущен!")
    print("Напиши 'exit' для выхода.\n")

    history = []

    while True:
        query = input("Ты: ")

        if query.lower() in ["exit", "quit"]:
            print("Выход из программы.")
            break

        # --- поиск контекста ---
        context, results = retrieve_context(query)

        # --- добавляем историю ---
        history.append(f"Пользователь: {query}")

        # --- формируем историю диалога ---
        history_text = "\n".join(history[-5:])  # последние 5 сообщений

        # --- объединяем с контекстом ---
        full_context = f"""
История диалога:
{history_text}

Контекст:
{context}
"""

        # --- генерация ответа ---
        answer = generate_answer(query, full_context)

        print(f"\nАссистент: {answer}\n")

        history.append(f"Ассистент: {answer}")


if __name__ == "__main__":
    main()