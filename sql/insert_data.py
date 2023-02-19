import sqlite3

with sqlite3.connect("dvdrent.db") as connection:
    cursor = connection.cursor()

        # insert data into tables

    connection.execute(
        "INSERT INTO author (full_name) VALUES ('John Peck'), ('Vanessa Doe'), ('Sirius Black'), ('Drake Bell')"
    )

    connection.execute(
        "INSERT INTO genre (name) VALUES ('Horror'), ('Comedy'), ('Action'), ('Drama'), ('Romance')"
    )

    connection.execute(
        "INSERT INTO main_actor (name, surname, age) VALUES ('John', 'Lacosta', 25), ('Will', 'Smith', 30), ('Dorethy', 'Black', 35), ('Jane', 'Stalone', 40)"
    )

    connection.execute('INSERT INTO adult_restriction (is_adult) VALUES ("Yes"), ("No")')

    connection.execute(
        "INSERT INTO dvd (title, year, author_id, genre_id, main_actor_id, adult_restriction_id) VALUES ('The Shining', 1980, 1, 1, 1, 1), ('The Shining 2', 1982, 2, 2, 2, 2), ('The Shining 3', 1984, 3, 3, 3, 1), ('The Shining 4', 1986, 4, 4, 4, 2)"
    )

    connection.commit()

    print("Data inserted successfully")
