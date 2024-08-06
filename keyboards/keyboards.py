import aiogram
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Внести данные"),
            KeyboardButton(text="Запросить данные"),
        ],
        [
          KeyboardButton(text="Проверить срок полезного испознания"),
          KeyboardButton(text="Автоуведомления"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите команду",
    selective=True,

)

insert_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить оборудование"),
            KeyboardButton(text="Добавить ИНН"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите команду",
    selective=True,

)

reg_kb = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Регистрация"),
    ]],
    resize_keyboard=True,
    one_time_keyboard=True,
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить номер", request_contact=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
