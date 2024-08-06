import sqlite3

# Подключение к базе данных (если файла базы данных нет, он будет создан)
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Создание таблицы Тип_номенклатуры
cursor.execute('''
CREATE TABLE IF NOT EXISTS Тип_номенклатуры (
    Тип TEXT PRIMARY KEY
);
''')

# Создание таблицы User
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    ФИО TEXT NOT NULL,
    Номер_телефона TEXT,
    tg_id TEXT PRIMARY KEY
);
''')

# Создание таблицы ИНН
cursor.execute('''
CREATE TABLE IF NOT EXISTS ИНН (
    Номер_ИНН TEXT PRIMARY KEY,
    Название_организации TEXT NOT NULL,
    Юр_Адрес TEXT NOT NULL,
    Контактные_данные TEXT NOT NULL,
    FOREIGN KEY (Контактные_данные) REFERENCES User (ФИО)
);
''')

# Создание таблицы Оборудование
cursor.execute('''
CREATE TABLE IF NOT EXISTS Оборудование (
    Номер_ИНН TEXT NOT NULL,
    Серийный_номер TEXT PRIMARY KEY,
    Тип_номенклатуры TEXT NOT NULL,
    Место_установки TEXT NOT NULL,
    Дата_установки TEXT NOT NULL,
    Срок_длительности INTEGER NOT NULL,
    FOREIGN KEY (Номер_ИНН) REFERENCES ИНН (Номер_ИНН),
    FOREIGN KEY (Тип_номенклатуры) REFERENCES Тип_номенклатуры (Тип)
);
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()