# Открываем файл для записи
with open("links_mark.txt", "w") as file:
    # Создаем список ссылок
    links = [
        "https://www.example1.com",
        "https://www.example2.com",
        "https://www.example3.com",
    ]

    # Записываем каждую ссылку в файл
    for link in links:
        file.write(link + "\n")
