import sqlite3

connection = sqlite3.connect("dvdrent.db")
cursor = connection.cursor()

# get data from tables by using JOIN statement and print it out in a nice way
cursor.execute(
    "SELECT dvd.title, dvd.year, author.full_name, genre.name, main_actor.name, main_actor.surname, main_actor.age, adult_restriction.is_adult FROM dvd JOIN author ON dvd.author_id = author.id JOIN genre ON dvd.genre_id = genre.id JOIN main_actor ON dvd.main_actor_id = main_actor.id JOIN adult_restriction ON dvd.adult_restriction_id = adult_restriction.id"
)

rows = cursor.fetchall()

for row in rows:
    print(row)


print("Data retrieved successfully")

connection.close()
