import asyncio
import config
from keyboards import keyboards
from aiogram import Bot, Dispatcher
from handlers import user_comands, insert_commands, insert_test



async def main():
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher()
    dp.include_routers(user_comands.router,insert_commands.router,insert_test.router)

    print("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
