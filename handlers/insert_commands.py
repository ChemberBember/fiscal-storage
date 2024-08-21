from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import states
import aiosqlite
import sql.db_get as db
from sql.db_get import user_in_db as only_registrated_user

REG_ACCESS_NUMBER = "123"

from keyboards import keyboards

router = Router()

@router.message(F.text == "Внести данные")
@only_registrated_user
async def choose_insert(message: Message, state: FSMContext):
    await message.reply("Выберите что вы хотите добавить", reply_markup=keyboards.insert_kb)

@router.message(F.text == "Добавить оборудование")
@only_registrated_user
async def add_new_device(message: Message, state: FSMContext):
    await state.set_state(states.UserInsertDeviceStates.ADD_SERIAL_NUMBER)
    await message.reply("Введите серийный номер оборудования")

@router.message(F.text == "Регистрация")
async def registration(message: Message, state: FSMContext):
    await state.set_state(states.Registration.REGISTRATION_NUMBER)
    await message.reply("Введите код доступа")

@router.message(states.Registration.REGISTRATION_NUMBER, F.text)
async def check_access(message: Message, state: FSMContext):
    if message.text == REG_ACCESS_NUMBER:
        await message.reply("Пожалуйста введите ФИО")
        await state.set_state(states.Registration.REGISTRATION)
    else:
        await message.reply("Неверный код доступа")
        await state.clear()



@router.message(states.Registration.REGISTRATION, F.text)
async def insert_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(states.Registration.PHONE)
    await message.reply("Пожалуйста предоставьте ваш номер телефона", reply_markup=keyboards.phone_kb)

@router.message(states.Registration.PHONE)
async def insert_phone(message: Message, state: FSMContext):
    async with aiosqlite.connect(r"C:\Users\siver\pythonProject\aiogram-bot\sqlite.db") as db:
        data = await state.get_data()
        await state.clear()
        try:
            await db.execute("INSERT INTO User (ФИО, Номер_телефона, tg_id) VALUES (?, ?, ?)",
                             (data["full_name"], message.contact.phone_number, message.from_user.id))
            await db.commit()
            await message.reply("Вы успешно зарегистрированы", reply_markup=keyboards.main_kb)
        except:
            await message.reply("Вы уже зарегистрированы")
            return

@router.message(F.text == "Добавить ИНН")
@only_registrated_user
async def insert_inn(message: Message, state: FSMContext):
    await message.reply("Введите ИНН")
    await state.set_state(states.UserInsertInnStates.ADD_NEW_INN)

@router.message(states.UserInsertInnStates.ADD_NEW_INN, F.text)
async def insert_inn(message: Message, state: FSMContext):
    await state.update_data(inn=message.text)
    await state.set_state(states.UserInsertInnStates.ADD_ORG_NAME)
    await message.reply("Введите название организации")

@router.message(states.UserInsertInnStates.ADD_ORG_NAME, F.text)
async def insert_org_name(message: Message, state: FSMContext):
    await state.update_data(org_name=message.text)
    await state.set_state(states.UserInsertInnStates.ADD_ADDRESS)
    await message.reply("Введите адрес")

@router.message(states.UserInsertInnStates.ADD_ADDRESS, F.text)
async def insert_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await db.insert_inn(data["inn"], data["org_name"], data["address"], message.from_user.id)
    await message.reply("ИНН успешно добавлен")
    await state.clear()
