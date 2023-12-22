import asyncio
import logging
import re

import aiogram
from aiogram import executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import backend
import config
import keyboards


class SelectAuto(StatesGroup):
    Brand = State()
    Model = State()
    Year = State()
    Mileage = State()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Initialize bot and dispatcher
bot = aiogram.Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.callback_query_handler(lambda query: query.data.startswith("cancel"), state='*')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Действие отменено'
    )


@dp.callback_query_handler(lambda query: query.data.startswith("back:"), state='*')
async def back(callback_query: CallbackQuery, state: FSMContext):
    back_target = callback_query.data.split(":")[1]
    if back_target == 'brand':
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите марку машины:',
            reply_markup=keyboards.generate_brands()
        )
        await SelectAuto.Brand.set()
    elif back_target == 'model':
        data = await state.get_data()
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите марку машины:',
            reply_markup=keyboards.generate_models(data['brand'])
        )
        await SelectAuto.Model.set()
    elif back_target == 'year':
        data = await state.get_data()
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text='Выберите год производства машины:',
            reply_markup=keyboards.generate_years(data['brand'], data['model'])
        )
    elif back_target == 'end':
        cnd = {
            0: 'Целые',
            1: 'Битые',
            'Не указано': 'Не указано'
        }
        data = await state.get_data()
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Текущая информация:\n'
                 f'Марка: {data["brand"]}\n'
                 f'Модель: {data["model"]}\n'
                 f'Год производства: {data["year"]}\n'
                 f'Пробег: {data["mileage"]} км.\n\n'
                 f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
                 f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
                 f'Тип кузова: {data.get("body_type", "Не указано")}\n'
                 f'Тип привода: {data.get("drive_type", "Не указано")}\n'
                 f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
                 f'Для точности расчёта вы можете добавить еще параметры.',
            reply_markup=keyboards.generate_extra_options(data)
        )


@dp.message_handler(commands=['start'])
async def cmd_start(message: aiogram.types.Message):
    await message.answer('Привет, выбери марку машины:', reply_markup=keyboards.generate_brands())
    await SelectAuto.Brand.set()


@dp.callback_query_handler(lambda query: query.data.startswith("brand:"), state=SelectAuto.Brand)
async def select_brand(callback_query: CallbackQuery, state: FSMContext):
    brand = callback_query.data.split(":")[1]

    await state.update_data(chat_id=callback_query.message.chat.id)
    await state.update_data(message_id=callback_query.message.message_id)

    await state.update_data(brand=brand)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите модель машины:',
        reply_markup=keyboards.generate_models(brand)
    )
    await SelectAuto.Model.set()


@dp.callback_query_handler(lambda query: query.data.startswith("model:"), state=SelectAuto.Model)
async def select_model(callback_query: CallbackQuery, state: FSMContext):
    model = callback_query.data.split(":")[1]
    await state.update_data(model=model)
    data = await state.get_data()
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Выберите год производства машины:',
        reply_markup=keyboards.generate_years(data['brand'], data['model'])
    )
    await SelectAuto.Year.set()


@dp.callback_query_handler(lambda query: query.data.startswith("year:"), state=SelectAuto.Year)
async def select_year(callback_query: CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    await state.update_data(year=int(year))
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text='Укажите пробег:',
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton('<< Назад', callback_data='back:year'),
            InlineKeyboardButton('Отмена', callback_data='cancel')
        )
    )
    await SelectAuto.Mileage.set()


@dp.message_handler(state=SelectAuto.Mileage)
async def select_mileage(message: aiogram.types.Message, state: FSMContext):

    if re.match('\\d+', message.text) is not None:
        await state.update_data(mileage=int(re.sub(' ', '', message.text)))
        data = await state.get_data()
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Текущая информация:\n'
                 f'Марка: {data["brand"]}\n'
                 f'Модель: {data["model"]}\n'
                 f'Год производства: {data["year"]}\n'
                 f'Пробег: {data["mileage"]} км.\n\n'
                 f'Для точности расчёта вы можете добавить еще параметры.',
            reply_markup=keyboards.generate_extra_options(data)
        )
    else:
        return await message.reply("Ты указал некорректный пробег, введи снова")


@dp.callback_query_handler(lambda query: query.data.startswith("extra:"), state='*')
async def select_extra(callback_query: CallbackQuery, state: FSMContext):
    extra_type = callback_query.data.split(":")[1]
    data = await state.get_data()
    if extra_type == 'Condition':
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Выберите состояние автомобиля',
            reply_markup=keyboards.generate_condition(data)
        )
    elif extra_type == 'Transmission':
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Выберите тип трансмиссии автомобиля',
            reply_markup=keyboards.generate_transmission(data)
        )
    elif extra_type == 'Body_type':
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Выберите тип кузова автомобиля',
            reply_markup=keyboards.generate_body_type(data)
        )
    elif extra_type == 'Drive_type':
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Выберите привод автомобиля',
            reply_markup=keyboards.generate_drive_type(data)
        )
    elif extra_type == 'Count_horsepower':
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text=f'Выберите количество лошадиных сил автомобиля',
            reply_markup=keyboards.generate_count_horsepower(data)
        )


@dp.callback_query_handler(lambda query: query.data.startswith("condition:"), state='*')
async def select_condition(callback_query: CallbackQuery, state: FSMContext):
    condition = callback_query.data.split(":")[1]
    await state.update_data(condition=int(condition))
    data = await state.get_data()
    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Текущая информация:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Для точности расчёта вы можете добавить еще параметры.',
        reply_markup=keyboards.generate_extra_options(data)
    )


@dp.callback_query_handler(lambda query: query.data.startswith("transmission:"), state='*')
async def select_transmission(callback_query: CallbackQuery, state: FSMContext):
    transmission = callback_query.data.split(":")[1]
    await state.update_data(transmission=transmission)
    data = await state.get_data()
    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Текущая информация:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Для точности расчёта вы можете добавить еще параметры.',
        reply_markup=keyboards.generate_extra_options(data)
    )


@dp.callback_query_handler(lambda query: query.data.startswith("body_type:"), state='*')
async def select_body_type(callback_query: CallbackQuery, state: FSMContext):
    body_type = callback_query.data.split(":")[1]
    await state.update_data(body_type=body_type)
    data = await state.get_data()
    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Текущая информация:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Для точности расчёта вы можете добавить еще параметры.',
        reply_markup=keyboards.generate_extra_options(data)
    )


@dp.callback_query_handler(lambda query: query.data.startswith("drive_type:"), state='*')
async def select_drive_type(callback_query: CallbackQuery, state: FSMContext):
    drive_type = callback_query.data.split(":")[1]
    await state.update_data(drive_type=drive_type)
    data = await state.get_data()
    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Текущая информация:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Для точности расчёта вы можете доавить еще параметры.',
        reply_markup=keyboards.generate_extra_options(data)
    )


@dp.callback_query_handler(lambda query: query.data.startswith("count_horsepower:"), state='*')
async def select_drive_type(callback_query: CallbackQuery, state: FSMContext):
    count_horsepower = callback_query.data.split(":")[1]
    await state.update_data(count_horsepower=int(count_horsepower))
    data = await state.get_data()
    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Текущая информация:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Для точности расчёта вы можете доавить еще параметры.',
        reply_markup=keyboards.generate_extra_options(data)
    )


@dp.callback_query_handler(lambda query: query.data.startswith("calculate"), state='*')
async def calculate(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    price = backend.calculate_price(data)

    cnd = {
        0: 'Целые',
        1: 'Битые',
        'Не указано': 'Не указано'
    }

    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['message_id'],
        text=f'Информация для расчёта:\n'
             f'Марка: {data["brand"]}\n'
             f'Модель: {data["model"]}\n'
             f'Год производства: {data["year"]}\n'
             f'Пробег: {data["mileage"]} км.\n\n'
             f'Состояние: {cnd.get(data.get("condition", "Не указано"), "Не указано")}\n'
             f'Тип трансмиссии: {data.get("transmission", "Не указано")}\n'
             f'Тип кузова: {data.get("body_type", "Не указано")}\n'
             f'Тип привода: {data.get("drive_type", "Не указано")}\n'
             f'Количество лошадиных сил: {data.get("count_horsepower", "Не указано")}\n\n'
             f'Результат:\n'
             f'💵Примерная цена: {price}₽'
    )
    await state.finish()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=False)
