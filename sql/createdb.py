import sqlite3

connection = sqlite3.connect("dvdrent.db")
print("Database opened successfully")
cursor = connection.cursor()

#delete
#cursor.execute('''DROP TABLE  ;)

# create tables
connection.execute(
    "create table app_author (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, full_name VARCHAR(25) NOT NULL)"
);

connection.execute(
    "create table app_genre (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name VARCHAR(12) NOT NULL)"
);

connection.execute(
    "create table app_main_actor (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name VARCHAR(10) NOT NULL, surname VARCHAR(10) NOT NULL, age INTEGER(2) NOT NULL)"
);

connection.execute(
    "create table app_adult_restriction (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, adult_movie BOOLEAN DEFAULT FALSE NOT NULL)"
);

connection.execute(
    "create table app_dvd (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, title TEXT(25) NOT NULL, year INTEGER(4) NOT NULL, author_id INTEGER REFERENCES app_author (author_id), genre_id INTEGER REFERENCES app_genre (genre_id), main_actor_id INTEGER REFERENCES app_main_actor (main_actor_id), adult_restriction_id INTEGER REFERENCES app_adult_restriction (adult_restriction_id))"
);

print("Tables created successfully")

connection.close()
   
print("Database closed successfully")
