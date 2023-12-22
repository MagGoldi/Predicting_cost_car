from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import backend


def generate_brands():
    brands = backend.get_brand()
    brands_keyboards = InlineKeyboardMarkup(row_width=1)
    for brand in brands:
        brands_keyboards.add(InlineKeyboardButton(
            text=brand, callback_data=f'brand:{brand}'))
    brands_keyboards.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))

    return brands_keyboards


def generate_models(brand):
    models = backend.get_model(brand)
    models_keyboard = InlineKeyboardMarkup(row_width=1)
    for model in models:
        models_keyboard.add(InlineKeyboardButton(
            text=model, callback_data=f'model:{model}'))
    models_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:brand'))
    models_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))

    return models_keyboard


def generate_years(brand, model):
    years = backend.get_year(brand, model)
    years_keyboard = InlineKeyboardMarkup(row_width=1)
    for year in range(years[1], years[0]-1, -1):
        years_keyboard.add(InlineKeyboardButton(
            text=f'{year}', callback_data=f'year:{year}'))
    years_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:model'))
    years_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))

    return years_keyboard


def generate_extra_options(data):
    options = backend.get_params(data)
    extra_options_keyboard = InlineKeyboardMarkup(row_width=1)
    translates = {
        'Condition': 'Состояние🚗',
        'Transmission': 'Трансмиссия⚙️',
        'Body_type': 'Тип кузова🚚',
        'Drive_type': 'Привод🚲',
        'Count_horsepower': 'Количество лошадиных сил🐎'
    }
    for option in options.keys():
        if len(options[option]) > 1 and (str(option).lower() not in data.keys()):
            extra_options_keyboard.add(InlineKeyboardButton(
                translates[option], callback_data=f'extra:{option}'))
        elif len(options[option]) <= 1 and option == 'Condition' and (str(option).lower() not in data.keys()):
            extra_options_keyboard.add(InlineKeyboardButton(
                'Состояние🚗', callback_data=f'extra:Condition'))
    extra_options_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))
    extra_options_keyboard.add(InlineKeyboardButton(
        text='Рассчитать стоимость', callback_data=f'calculate'))

    return extra_options_keyboard


def generate_condition(data):
    conditions_keyboard = InlineKeyboardMarkup(row_width=1)
    conditions_keyboard.add(InlineKeyboardButton(
        'Целые', callback_data=f'condition:{0}'))
    conditions_keyboard.add(InlineKeyboardButton(
        'Битые', callback_data=f'condition:{1}'))
    conditions_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))
    conditions_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:end'))

    return conditions_keyboard


def generate_transmission(data):
    transmissions = backend.get_params(data)['Transmission']
    transmissions_keyboard = InlineKeyboardMarkup(row_width=1)
    for transmission in transmissions:
        transmissions_keyboard.add(InlineKeyboardButton(
            transmission, callback_data=f'transmission:{transmission}'))
    transmissions_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))
    transmissions_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:end'))
    return transmissions_keyboard


def generate_body_type(data):
    body_types = backend.get_params(data)['Body_type']
    body_types_keyboard = InlineKeyboardMarkup(row_width=1)
    for body_type in body_types:
        body_types_keyboard.add(InlineKeyboardButton(
            body_type, callback_data=f'body_type:{body_type}'))
    body_types_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))
    body_types_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:end'))
    return body_types_keyboard


def generate_drive_type(data):
    drive_types = backend.get_params(data)['Drive_type']
    drive_types_keyboard = InlineKeyboardMarkup(row_width=1)
    for drive_type in drive_types:
        drive_types_keyboard.add(InlineKeyboardButton(
            drive_type, callback_data=f'drive_type:{drive_type}'))
    drive_types_keyboard.add(InlineKeyboardButton(
        text='Отмена', callback_data=f'cancel'))
    drive_types_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:end'))
    return drive_types_keyboard


def generate_count_horsepower(data):
    count_horsepower_types = backend.get_params(data)['Count_horsepower']
    count_horsepower_types_keyboard = InlineKeyboardMarkup(row_width=1)
    print(count_horsepower_types)
    for item in count_horsepower_types:
        count_horsepower_types_keyboard.add(InlineKeyboardButton(
            f'{item}', callback_data=f'count_horsepower:{item}'))
    count_horsepower_types_keyboard.add(
        InlineKeyboardButton(text='Отмена', callback_data=f'cancel'))
    count_horsepower_types_keyboard.add(InlineKeyboardButton(
        text='<< Назад', callback_data=f'back:end'))
    return count_horsepower_types_keyboard
