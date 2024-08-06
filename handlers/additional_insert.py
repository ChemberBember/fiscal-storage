from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from utils import states
import aiosqlite
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton



MAIN_MENU = 'main_menu'
BOT_BUTTONS = 'bot_buttons'
ENTER_DATA = 'enter_data'
ENTER_INN_DATA = 'enter_inn_data'
ENTER_EQUIPMENT_DATA = 'enter_equipment_data'
REQUEST_DATA = 'request_data'
ENTER_CONTACT_DATA = 'enter_contact_data'
ENTER_ORG_ADDRESS = 'enter_org_address'
ENTER_ORG_NAME = 'enter_org_name'
ENTER_SERIAL_NUMBER = 'enter_serial_number'
ENTER_INSTALL_DATE = 'enter_install_date'
ENTER_USAGE_PERIOD = 'enter_usage_period'
ENTER_NOMENCLATURE_TYPE = 'enter_nomenclature_type'
SELECT_NOMENCLATURE_TYPE = 'select_nomenclature_type'
ADD_NEW_NOMENCLATURE_TYPE = 'add_new_nomenclature_type'

# State storage
user_states = {}
user_data = {}

router = Router()

def get_user_state(user_id):
    return user_states.get(user_id, MAIN_MENU)

def update_user_state(user_id, state):
    user_states[user_id] = state

def get_user_data(user_id, key, default=None):
    return user_data.get(user_id, {}).get(key, default)

def update_user_data(user_id, key, value):
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id][key] = value

# Entry point to bot settings, sets the user's state to BOT_BUTTONS

# Handler for "Внести данные"
@router.message(lambda message: message.text == "Внести данные")
async def enter_data(message: Message):
    update_user_state(message.from_user.id, ENTER_DATA)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ИНН")],
            [KeyboardButton(text="Добавить оборудование по серийному номеру")],
            [KeyboardButton(text="Назад")],  # Adding a "Back" button to return to the main menu
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите, что вы хотите добавить:", reply_markup=keyboard)

# Handler for "Добавить ИНН"
@router.message(lambda message: message.text == "Добавить ИНН")
async def add_inn(message: Message):
    update_user_state(message.from_user.id, ENTER_INN_DATA)
    await message.answer("Введите ИНН:")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_INN_DATA)
async def enter_inn_data(message: Message):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("SELECT Номер_ИНН FROM ИНН WHERE Номер_ИНН = ?", (message.text,)) as cursor:
            inn_exists = await cursor.fetchone()
            if inn_exists:
                await message.answer("Такой ИНН уже зарегистрирован. Введите другой ИНН:")
                return
    update_user_data(message.from_user.id, 'inn', message.text)
    update_user_state(message.from_user.id, ENTER_ORG_NAME)
    await message.answer("Введите название организации:")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_ORG_NAME)
async def enter_org_name(message: Message):
    update_user_data(message.from_user.id, 'org_name', message.text)
    update_user_state(message.from_user.id, ENTER_ORG_ADDRESS)
    await message.answer("Введите юридический адрес организации:")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_ORG_ADDRESS)
async def enter_org_address(message: Message):
    update_user_data(message.from_user.id, 'org_address', message.text)
    async with aiosqlite.connect('sqlite.db') as db:
        fio = db.execute("SELECT ФИО FROM User WHERE tg_id = ?", (message.from_user.id,))

        await db.execute("INSERT INTO ИНН (Номер_ИНН, Название_организации,"
                         " Юр_Адрес, Контактные_данные) VALUES (?, ?, ?, ?)",
                         (get_user_data(message.from_user.id, 'inn'),
                          get_user_data(message.from_user.id, 'org_name'),
                        get_user_data(message.from_user.id, 'org_address'), fio[0]))
        await db.commit()
    await message.answer("ИНН успешно добавлен!")



# Handler for "Добавить оборудование по серийному номеру"
@router.message(lambda message: message.text == "Добавить оборудование по серийному номеру")
async def add_equipment(message: Message):
    update_user_state(message.from_user.id, ENTER_EQUIPMENT_DATA)
    await message.answer("Введите ИНН:")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_EQUIPMENT_DATA)
async def enter_equipment_data(message: Message):
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("SELECT Номер_ИНН FROM ИНН WHERE Номер_ИНН = ?", (message.text,)) as cursor:
            inn_exists = await cursor.fetchone()
            if not inn_exists:
                await message.answer("ИНН не найден. Введите зарегистрированный ИНН:")
                return
    update_user_data(message.from_user.id, 'inn', message.text)
    update_user_state(message.from_user.id, ENTER_SERIAL_NUMBER)
    await message.answer("Введите серийный номер оборудования:")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_SERIAL_NUMBER)
async def enter_serial_number(message: Message):
    update_user_data(message.from_user.id, 'serial_number', message.text)
    update_user_state(message.from_user.id, ENTER_INSTALL_DATE)
    await message.answer("Введите дату установки (в формате ДД.ММ.ГГ):")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_INSTALL_DATE)
async def enter_install_date(message: Message):
    update_user_data(message.from_user.id, 'install_date', message.text)
    update_user_state(message.from_user.id, ENTER_USAGE_PERIOD)
    await message.answer("Введите срок полезного использования (в месяцах):")

@router.message(lambda message: get_user_state(message.from_user.id) == ENTER_USAGE_PERIOD)
async def enter_usage_period(message: Message):
    update_user_data(message.from_user.id, 'usage_period', message.text)
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("SELECT Тип FROM Тип_номенклатуры") as cursor:
            types = await cursor.fetchall()
            if types:
                types_buttons = [KeyboardButton(text=type[0]) for type in types]
                types_buttons.append(KeyboardButton(text="Другой"))
                keyboard = ReplyKeyboardMarkup(keyboard=[types_buttons], resize_keyboard=True)
                update_user_state(message.from_user.id, SELECT_NOMENCLATURE_TYPE)
                await message.answer("Выберите тип номенклатуры:", reply_markup=keyboard)
            else:
                update_user_state(message.from_user.id, ADD_NEW_NOMENCLATURE_TYPE)
                await message.answer("Введите тип номенклатуры (в базе данных нет ни одного типа):")

@router.message(lambda message: get_user_state(message.from_user.id) == SELECT_NOMENCLATURE_TYPE)
async def select_nomenclature_type(message: Message):
    if message.text == "Другой":
        update_user_state(message.from_user.id, ADD_NEW_NOMENCLATURE_TYPE)
        await message.answer("Введите тип номенклатуры:")
    else:
        async with aiosqlite.connect('sqlite.db') as db:
            await db.execute(
                "INSERT INTO Оборудование (Номер_ИНН, Серийный_номер, Тип_номенклатуры, Место_установки, Дата_установки, Срок_длительности) VALUES (?, ?, ?, ?, ?, ?)",
                (get_user_data(message.from_user.id, 'inn'), get_user_data(message.from_user.id, 'serial_number'), message.text, "Место установки", get_user_data(message.from_user.id, 'install_date'), get_user_data(message.from_user.id, 'usage_period'))
            )
            await db.commit()
        await message.answer("Оборудование успешно добавлено!")
        update_user_state(message.from_user.id, BOT_BUTTONS)

@router.message(lambda message: get_user_state(message.from_user.id) == ADD_NEW_NOMENCLATURE_TYPE)
async def add_new_nomenclature_type(message: Message):
    async with aiosqlite.connect('sqlite.db') as db:
        await db.execute(
            "INSERT INTO Тип_номенклатуры (Тип) VALUES (?)",
            (message.text,)
        )
        await db.commit()
        await db.execute(
            "INSERT INTO Оборудование (Номер_ИНН, Серийный_номер, Тип_номенклатуры, Место_установки, Дата_установки, Срок_длительности) VALUES (?, ?, ?, ?, ?, ?)",
            (get_user_data(message.from_user.id, 'inn'), get_user_data(message.from_user.id, 'serial_number'), message.text, "Место установки", get_user_data(message.from_user.id, 'install_date'), get_user_data(message.from_user.id, 'usage_period'))
        )
        await db.commit()
    await message.answer("Оборудование успешно добавлено!")
    update_user_state(message.from_user.id, BOT_BUTTONS)

# Handler for "Запросить данные"
@router.message(lambda message: message.text == "Запросить данные")
async def request_data(message: Message):
    update_user_state(message.from_user.id, REQUEST_DATA)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить данные по серийному номеру")],
            [KeyboardButton(text="Получить данные по ИНН")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите способ получения данных:", reply_markup=keyboard)

# Handler for "Получить данные по серийному номеру"
@router.message(lambda message: message.text == "Получить данные по серийному номеру")
async def get_data_by_serial_number(message: Message):
    update_user_state(message.from_user.id, 'get_serial_number')
    await message.answer("Введите серийный номер для получения данных:")

@router.message(lambda message: get_user_state(message.from_user.id) == 'get_serial_number')
async def fetch_data_by_serial_number(message: Message):
    serial_number = message.text
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("SELECT * FROM Оборудование WHERE Серийный_номер = ?", (serial_number,)) as cursor:
            equipment = await cursor.fetchone()
            if equipment:
                await message.answer(f"ИНН: {equipment[0]}\nСерийный номер: {equipment[1]}\nТип номенклатуры: {equipment[2]}\nМесто установки: {equipment[3]}\nДата установки: {equipment[4]}\nСрок длительности: {equipment[5]}")
            else:
                await message.answer("Оборудование с таким серийным номером не найдено.")
    update_user_state(message.from_user.id, BOT_BUTTONS)

# Handler for "Получить данные по ИНН"
@router.message(lambda message: message.text == "Получить данные по ИНН")
async def get_data_by_inn(message: Message):
    update_user_state(message.from_user.id, 'get_inn')
    await message.answer("Введите ИНН для получения данных:")

@router.message(lambda message: get_user_state(message.from_user.id) == 'get_inn')
async def fetch_data_by_inn(message: Message):
    inn = message.text
    async with aiosqlite.connect('sqlite.db') as db:
        async with db.execute("SELECT * FROM ИНН WHERE Номер_ИНН = ?", (inn,)) as cursor:
            inn_data = await cursor.fetchone()
            if inn_data:
                async with db.execute("SELECT * FROM User WHERE ФИО = ?", (inn_data[3],)) as user_cursor:
                    user_data = await user_cursor.fetchone()
                    async with db.execute("SELECT Серийный_номер FROM Оборудование WHERE Номер_ИНН = ?", (inn,)) as equipment_cursor:
                        equipment = await equipment_cursor.fetchall()
                        serial_numbers = ', '.join([eq[0] for eq in equipment])
                        await message.answer(f"Название организации: {inn_data[1]}\nЮр. адрес: {inn_data[2]}\nКонтактные данные: {user_data[0]} / {user_data[1]}\nСерийные номера оборудования: {serial_numbers}")
            else:
                await message.answer("ИНН не найден.")
    update_user_state(message.from_user.id, BOT_BUTTONS)

# Handler for "Назад" button to return to the main menu
@router.message(lambda message: message.text == "Назад")
async def back_to_main_menu(message: Message):
    update_user_state(message.from_user.id, BOT_BUTTONS)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Внести данные")],
            [KeyboardButton(text="Запросить данные")],
            [KeyboardButton(text="Проверить подписку")],
            [KeyboardButton(text="Включить автоуведомления")],
        ],
        resize_keyboard=True
    )
    await message.answer("Вы вернулись в главное меню:", reply_markup=keyboard)