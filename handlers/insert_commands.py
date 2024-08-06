from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from utils import states
from sql import executor


from keyboards import keyboards

router = Router()

@router.message(F.text == "Внести данные")
async def choose_insert(message: Message, state: FSMContext):
    await message.reply("Выберите что вы хотите добавить", reply_markup=keyboards.insert_kb)

@router.message(F.text == "Добавить оборудование")
async def add_new_device(message: Message, state: FSMContext):
    await state.set_state(states.UserInsertDeviceStates.ADD_SERIAL_NUMBER)
    await message.reply("Введите серийный номер оборудования")

@router.message(F.text == "Регистрация")
async def registration(message: Message, state: FSMContext):
    await state.set_state(states.Registration.REGISTRATION)
    await message.reply("Введите ваше ФИО")


@router.message(states.Registration.REGISTRATION, F.text)
async def insert_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(states.Registration.PHONE)
    await message.reply("Пожалуйста предоставьте ваш номер телефона", reply_markup=keyboards.phone_kb)

@router.message(states.Registration.PHONE)
async def insert_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data["full_name"])
    print(message.contact.phone_number)
    print(message.from_user.id)





@router.message(states.UserInsertDeviceStates.ADD_SERIAL_NUMBER)
async def add_serial_number(message: Message, state: FSMContext):
    await state.update_data(serial_number=message.text)
