import aiosqlite
import asyncio

FILE_PATH = r'C:\Users\siver\pythonProject\aiogram-bot\sqlite.db'
async def create_tables():
 async with aiosqlite.connect(FILE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS INN (
                Номер_ИНН TEXT PRIMARY KEY,
                Название_организации TEXT,
                Юр_Адрес TEXT,
                Контактные_данные TEXT,
                FOREIGN KEY (Контактные_данные) REFERENCES User(tg_id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Оборудование (
                Номер_ИНН TEXT,
                Серийный_номер TEXT PRIMARY KEY,
                Тип_номенклатуры TEXT,
                Место_установки TEXT,
                Дата_установки TEXT,
                Срок_длительности TEXT,
                FOREIGN KEY (Номер_ИНН) REFERENCES ИНН(НомерИНН),
                FOREIGN KEY (Тип_номенклатуры) REFERENCES Тип_номенклатуры(Тип)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS Тип_номенклатуры (
                Тип TEXT PRIMARY KEY
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS User (
                ФИО TEXT PRIMARY KEY,
                Номер_телефона TEXT,
                tg_id INTEGER
            )
        ''')
        await db.commit()



asyncio.run(create_tables())

