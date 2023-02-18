import sqlite3

with sqlite3.connect("dvdrent.db") as connection:
    cursor = connection.cursor()

    # create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS genre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS main_actor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        age INTEGER NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS adult_restriction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_adult BOOLEAN DEFAULT FALSE NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dvd (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER NOT NULL,
        author_id INTEGER REFERENCES author (id),
        genre_id INTEGER REFERENCES genre (id),
        main_actor_id INTEGER REFERENCES main_actor (id),
        adult_restriction_id INTEGER REFERENCES adult_restriction (id)
    )''')

    # enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")

print("Tables created successfully")
