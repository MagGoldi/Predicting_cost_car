import csv
import datetime

# Создаем название файла с текущей датой
filename = "car_data_" + str(datetime.date.today())
print(filename)
# Создаем файл и записываем в него данные
# with open(filename, mode='w', newline='') as file:
