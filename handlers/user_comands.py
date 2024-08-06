from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import keyboards
import aiosqlite

router = Router()

temporary_data = []

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with aiosqlite.connect('sqlite.db') as db:
        cursor = await db.execute(f"SELECT 1 FROM User WHERE tg_id = {message.from_user.id}")
        isRegistered = await cursor.fetchone()
    if isRegistered:
        await message.answer("Добро пожаловать", reply_markup=keyboards.main_kb)
    else:
        await message.answer("Приветствую!", reply_markup=keyboards.reg_kb)
