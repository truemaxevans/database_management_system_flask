import sqlite3

connection = sqlite3.connect("dvdrent.db")
print("Database opened successfully")

cursor = connection.cursor()

# insert data into tables

connection.execute(
    "insert into app_author (full_name) values ('John Peck'), ('Vanessa Doe'), ('Sirius Black'), ('Drake Bell')"
)

connection.execute(
    "insert into app_genre (name) values ('Horror'), ('Comedy'), ('Action'), ('Drama'), ('Romance')"
)

connection.execute(
    "insert into app_main_actor (name, surname, age) values ('John', 'Lacosta', 25), ('Will', 'Smith', 30), ('Dorethy', 'Black', 35), ('Jane', 'Stalone', 40)"
)

connection.execute("insert into app_adult_restriction (adult_movie) values (0), (1)")

connection.execute(
    "insert into app_dvd (title, year, author_id, genre_id, main_actor_id, adult_restriction_id) values ('The Shining', 1980, 1, 1, 1, 1), ('The Shining 2', 1982, 2, 2, 2, 2), ('The Shining 3', 1984, 3, 3, 3, 1), ('The Shining 4', 1986, 4, 4, 4, 2)"
)

connection.commit()

print("Data inserted successfully")

connection.close()

print("Database closed successfully")
