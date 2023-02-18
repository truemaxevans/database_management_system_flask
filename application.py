# importing necessary libraries
import datetime
import logging
import sqlite3

import pandas as pd
from flask import Flask, render_template, request, send_file


# creating a Flask app
app = Flask(__name__)


# logging configuration
app.logger.setLevel(logging.INFO)


# rendering html templates with url
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_dvd")
def add_dvd():
    return render_template("add_dvd.html")


@app.route("/get_dvd")
def get_dvd():
    return render_template("get_dvd.html")


@app.route("/delete_dvd")
def delete_dvd():
    return render_template("delete_dvd.html")


@app.route("/update_dvd")
def update_dvd():
    return render_template("update_dvd.html")


# run SQL execution in functions and return results
@app.route("/get_dvd_entries", methods=["GET"])
def get_all_dvd():
    try:
        conn = sqlite3.connect("dvdrent.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT dvd.title, dvd.year, author.full_name, genre.name, main_actor.surname, adult_restriction.is_adult FROM dvd JOIN author ON dvd.author_id = author.id JOIN genre ON dvd.genre_id = genre.id JOIN main_actor ON dvd.main_actor_id = main_actor.id JOIN adult_restriction ON dvd.adult_restriction_id = adult_restriction.id"
        )
        rows = cur.fetchall()
        app.logger.info("Get all dvd entries successfully")
        return render_template("get_dvd.html", rows=rows)
    except Exception as e:
        app.logger.error(f"Error getting all dvd entries: {e}")
        return "An error occurred while retrieving the DVD entries."


@app.route("/add_entry", methods=["POST"])
def add_entry():
    try:
        title = request.form["title"]
        year = request.form["year"]
        author_name = request.form["author_name"]
        genre_name = request.form["genre_name"]
        main_actor = request.form["main_actor_surname"]
        is_adult = request.form["is_adult"]

        with sqlite3.connect("dvdrent.db") as connection:
            cur = connection.cursor()

            # check if author exists
            cur.execute("SELECT id FROM author WHERE full_name=?", (author_name,))
            author_id = cur.fetchone()
            if not author_id:
                # insert new author
                cur.execute("INSERT INTO author (full_name) VALUES (?)", (author_name,))
                author_id = cur.lastrowid
            else:
                author_id = author_id[0]

            # check if genre exists
            cur.execute("SELECT id FROM genre WHERE name=?", (genre_name,))
            genre_id = cur.fetchone()
            if not genre_id:
                # insert new genre
                cur.execute("INSERT INTO genre (name) VALUES (?)", (genre_name,))
                genre_id = cur.lastrowid
            else:
                genre_id = genre_id[0]

            # check if main actor exists
            cur.execute("SELECT id FROM main_actor WHERE surname=?", (main_actor,))
            main_actor_id = cur.fetchone()
            if not main_actor_id:
                # insert new main actor
                cur.execute("INSERT INTO main_actor (surname) VALUES (?)", (main_actor,))
                main_actor_id = cur.lastrowid
            else:
                main_actor_id = main_actor_id[0]

            # check if adult restriction exists
            cur.execute("SELECT id FROM adult_restriction WHERE is_adult=?", (is_adult,))
            adult_restriction_id = cur.fetchone()
            if not adult_restriction_id:
                # insert new adult restriction
                cur.execute("INSERT INTO adult_restriction (is_adult) VALUES (?)", (is_adult,))
                adult_restriction_id = cur.lastrowid
            else:
                adult_restriction_id = adult_restriction_id[0]

            # insert new dvd entry
            cur.execute(
                "INSERT INTO dvd (title, year, author_id, genre_id, main_actor_id, adult_restriction_id) VALUES (?, ?, ?, ?, ?, ?)",
                (title, year, author_id, genre_id, main_actor_id, adult_restriction_id),
            )
            connection.commit()
            app.logger.info("New dvd entry added successfully")
            return render_template("added_sucess.html")
    except Exception as e:
        app.logger.error(f"Error adding a new dvd entry: {e}")
        return "An error occurred while adding a new DVD entry."


@app.route("/delete_dvd_entry", methods=["POST"])
def delete_dvd_entry():
    try:
        title = request.form["title"]
        with sqlite3.connect("dvdrent.db") as connection:
            cur = connection.cursor()
            cur.execute("DELETE FROM dvd WHERE title = ?", (title,))
            connection.commit()
            app.logger.info("Dvd entry deleted successfully")
            return render_template("delete_sucess.html")
    except Exception as e:
        app.logger.error("Error while deleting dvd entry: {e}")
        return "An error occurred while deleting a DVD entry."


@app.route("/update_dvd_entry", methods=["POST"])
def update_dvd_entry():
    try:
        title = request.form["title"]
        year = request.form["year"]
        author = request.form["author_id"]
        genre = request.form["genre_id"]
        main_actor = request.form["main_actor_id"]
        adult_restriction = request.form["adult_restriction_id"]
        with sqlite3.connect("dvdrent.db") as connection:
            cur = connection.cursor()
            # update record by title
            cur.execute(
                "UPDATE dvd SET year = ?, author_id = ?, genre_id = ?, main_actor_id = ?, adult_restriction_id = ? WHERE title = ?",
                (year, author, genre, main_actor, adult_restriction, title),
            )
            connection.commit()
            app.logger.info("Dvd entry updated successfully")
            return render_template("index.html")
    except Exception as e:
        app.logger.error(f"Error updating dvd entry: {e}")
        return "An error occurred while updating a DVD entry."


# download all data from database as csv file using pandas
@app.route("/download_data_in_csv", methods=["GET"])
def download_data_in_csv():
    try:
        conn = sqlite3.connect("dvdrent.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT dvd.title, dvd.year, author.full_name, genre.name, main_actor.name, main_actor.surname, main_actor.age, adult_restriction.is_adult FROM dvd JOIN author ON dvd.author_id = author.id JOIN genre ON dvd.genre_id = genre.id JOIN main_actor ON dvd.main_actor_id = main_actor.id JOIN adult_restriction ON dvd.adult_restriction_id = adult_restriction.id"
        )
        rows = cur.fetchall()
        headers = [i[0] for i in cur.description]
        headers_upper = [i.upper() for i in headers]
        df = pd.DataFrame(rows, columns=headers_upper)
        app.logger.info("Download data in csv file successfully")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        df.to_csv(f"dvd_report_{current_date}.csv", index=False)
        return send_file(f"dvd_report_{current_date}.csv", as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error downloading data in csv file: {e}")
        return "An error occurred while downloading data in csv file."


# running the app
if __name__ == "__main__":
    app.run(debug=True)
