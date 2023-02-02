import sqlite3
if 1 == 11:
    cards = [
    ("id", "name", "spotify", "playlist", "action"),
    ("id2", "name2", "other", "track", "action2")
    ]

    connection = sqlite3.connect("card_list.db")
    cursor = connection.cursor()

    cursor.execute('create table cards (id INTEGER PRIMARY KEY AUTOINCREMENT, identity TEXT, name TEXT, service TEXT, type TEXT, action TEXT, notes TEXT, image TEXT)')
    cursor.executemany("insert into cards (identity, name, service, type, action) values (?,?,?,?,?)", cards)
    print("added ", cards)

    connection.commit()
    connection.close()

connection = sqlite3.connect("card_list.db")
cursor = connection.cursor()

for row in cursor.execute("SELECT * FROM cards"):
    print(row)

connection.commit()
connection.close()