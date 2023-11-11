import csv

columns = [
    "bodyType",
    "brand",
    "color",
    "fuelType",
    "modelDate",
    "name",
    "numberOfDoors",
    "productionDate",
    "vehicleConfiguration",
    "vehicleTransmission",
    "engineDisplacement",
    "enginePower",
    "description",
    "mileage",
    "Комплектация",
    "Привод",
    "Руль",
    "Состояние",
    "Владельцы",
    "ПТС",
    "Таможня",
    "Владение",
]
filename = "Parsing\dataset.csv"


def write_columns_to_csv(columns, filename):
    with open(file=filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)


write_columns_to_csv(columns, filename)
