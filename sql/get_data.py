import sqlite3

# Connect to the database using a context manager
with sqlite3.connect("dvdrent.db") as connection:
    # Create a cursor using a context manager
    cursor = connection.cursor()
        # Select data using JOIN statements
    cursor.execute(
        """
        SELECT
            dvd.title,
            dvd.year,
            author.full_name,
            genre.name,
            main_actor.name,
            main_actor.surname,
            main_actor.age,
            adult_restriction.is_adult
        FROM
            dvd
            JOIN author ON dvd.author_id = author.id
            JOIN genre ON dvd.genre_id = genre.id
            JOIN main_actor ON dvd.main_actor_id = main_actor.id
            JOIN adult_restriction ON dvd.adult_restriction_id = adult_restriction.id
        """
    )

    # Fetch all rows from the cursor and print the data
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# The connection is automatically closed when the context manager exits
