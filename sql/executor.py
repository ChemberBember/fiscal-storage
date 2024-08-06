import sqlite3



def INSERT_USER(FULL_NAME,PHONE,TG_ID):
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User VALUES(?,?,?)",(FULL_NAME,PHONE,TG_ID))
    conn.commit()
    conn.close()

conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Запрос для извлечения всех таблиц в базе данных
cursor.execute('''
SELECT name FROM sqlite_master WHERE type='table';
''')

# Извлечение всех строк результата запроса
tables = cursor.fetchall()

# Печать всех имен таблиц
print("Таблицы в базе данных:")
for table in tables:
    print(table[0])

# Закрытие соединения
conn.close()