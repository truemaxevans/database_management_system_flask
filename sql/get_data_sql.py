import sqlite3

connection = sqlite3.connect("dvdrent.db")
print("Database opened successfully")

cursor = connection.cursor()

# get data from tables by using JOIN statement and print it out in a nice way
cursor.execute(
    "SELECT app_dvd.title, app_dvd.year, app_author.full_name, app_genre.name, app_main_actor.name, app_main_actor.surname, app_main_actor.age, app_adult_restriction.adult_movie FROM app_dvd JOIN app_author ON app_dvd.author_id = app_author.id JOIN app_genre ON app_dvd.genre_id = app_genre.id JOIN app_main_actor ON app_dvd.main_actor_id = app_main_actor.id JOIN app_adult_restriction ON app_dvd.adult_restriction_id = app_adult_restriction.id"
);

rows = cursor.fetchall()

for row in rows:
    print(row)


print("Data retrieved successfully")

connection.close()

print("Database closed successfully")
