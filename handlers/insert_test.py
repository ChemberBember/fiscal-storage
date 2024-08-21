from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils import states
import aiosqlite
import sql.db_get as db
from sql.db_get import user_in_db as only_registrated_user
from keyboards import keyboards
router = Router()

# @router.message(F.text == "test")
# @only_registrated_user
# async def choose_insert(message: Message, state: FSMContext):
#     await message.reply("Выберите что вы хотите добавить", reply_markup=keyboards.test_kb)
#
# @router.message(F.text == "Добавить оборудование")
# @only_registrated_user
# async def add_new_device(message: Message, state: FSMContext):
#     await state.set_state(states.UserInsertDeviceStates.ADD_SERIAL_NUMBER)
#     await message.reply("Введите серийный номер оборудования")