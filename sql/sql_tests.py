import aiosqlite
import asyncio

async def test():
    async with aiosqlite.connect('../sqlite.db') as db:
        await db.execute(f"""INSERT OR REPLACE INTO INN (Номер_ИНН, Название_организации, Юр_Адрес, Контактные_данные)
            VALUES (?, ?, ?, ?)""", ('406', 'test', 'test', '660142115'))
        await db.commit()

asyncio.run(test())