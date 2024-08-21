import aiosqlite
from functools import wraps
from aiogram import types

FILE_PATH = r'C:\Users\siver\pythonProject\aiogram-bot\sqlite.db'

async def is_user_in_db(user_id: int) -> bool:
    try:
        async with aiosqlite.connect(FILE_PATH) as db:
            async with db.execute("SELECT 1 FROM User WHERE tg_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                return result is not None
    except:
        return False

def user_in_db(handler):
    @wraps(handler)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        if await is_user_in_db(user_id):
            return await handler(message, *args, **kwargs)
        else:
            await message.answer("Вы не авторизованы для выполнения этой команды.")
    return wrapper


async def get_user(id):
    async with aiosqlite.connect(FILE_PATH) as db:
        cursor = await db.execute(f"SELECT * FROM User")
        user = await cursor.fetchone()
        print(user)
        return user

async def get_inn(inn):
    async with aiosqlite.connect(FILE_PATH) as db:
        cursor = await db.execute(f"SELECT * FROM INN WHERE Номер_ИНН = {inn}")
        inn = await cursor.fetchone()
        return inn

async def get_types():
    async with aiosqlite.connect(FILE_PATH) as db:
        cursor = await db.execute(f"SELECT * FROM Тип_номенклатуры")
        types = await cursor.fetchall()
        return types

async def get_device(serial_number = None, inn = None):
    if serial_number:
        async with aiosqlite.connect(FILE_PATH) as db:
            cursor = await db.execute(f"SELECT * FROM Оборудование WHERE Серийный_номер = {serial_number}")
            device = await cursor.fetchone()
            return device
    if inn:
        async with aiosqlite.connect(FILE_PATH) as db:
            cursor = await db.execute(f"SELECT * FROM Оборудование WHERE Номер_ИНН = {inn}")
            device = await cursor.fetchone()
            return device

async def add_type(name):
    async with aiosqlite.connect(FILE_PATH) as db:
        await db.execute(f"INSERT INTO Тип_номенклатуры VALUES (?)",
                                  (name,))
        await db.commit()

async def add_device(serial_number, inn, type, install_date, usage_period,adress):
    async with aiosqlite.connect(FILE_PATH) as db:
        await db.execute(f"INSERT INTO Оборудование VALUES (?, ?, ?, ?, ?)",
                        (serial_number, inn, type, adress, install_date, usage_period))
        await db.commit()

# @router.message(states.Registration.PHONE)
# async def insert_phone(message: Message, state: FSMContext):
#     async with aiosqlite.connect('sqlite.db') as db:
#         data = await state.get_data()
#         await state.clear()
#         try:
#             await db.execute("INSERT INTO User (ФИО, Номер_телефона, tg_id) VALUES (?, ?, ?)",
#                              (data["full_name"], message.contact.phone_number, message.from_user.id))
#             await db.commit()
#             await message.reply("Вы успешно зарегистрированы", reply_markup=keyboards.main_kb)
#         except:
#             await message.reply("Вы уже зарегистрированы")
#             return


async def insert_inn(inn_number, organization_name, legal_address, contact_details):
    async with aiosqlite.connect(FILE_PATH) as db:
        await db.execute(f"""INSERT INTO INN (Номер_ИНН, Название_организации, Юр_Адрес, Контактные_данные)
            VALUES (?, ?, ?, ?)""", (inn_number, organization_name, legal_address, contact_details))

        await db.commit()
        print('inserted')