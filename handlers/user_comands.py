from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import keyboards

router = Router()

temporary_data = []

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in temporary_data:
        await message.answer("Вы уже вошли в систему", reply_markup=keyboards.main_kb)
    else:
        await message.answer("Приветствую!", reply_markup=keyboards.reg_kb)
