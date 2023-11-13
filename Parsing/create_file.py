import csv

car_info = {
    "Цена": 2263900,
    "Марка": "Toyota",
    "Модель": "Camry",
    "Год выпуска": 2015,
    "Поколение": "V50",
    "Пробег": 80000,
    "Владельцев по ПТС": 2,
    "Состояние": "Отличное",
    "Модификация": "2.5 AT (181 л.с.)",
    "Объём двигателя": 2.5,
    "Тип двигателя": "Бензин",
    "Коробка передач": "Автомат",
    "Привод": "Полный",
    "Комплектация": "Elegance",
    "Тип кузова": "Седан",
    "Цвет": "Серый",
    "Руль": "Левый",
    "Обмен": "Возможен",
    "Ссылка": "http://example.com/car",
}

car_url = car_info["Ссылка"]

with open("file.csv", "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=car_info.keys())
    writer.writerow(car_info)
