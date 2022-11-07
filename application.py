# importing necessary libraries
import sqlite3
import pandas as pd

from logging import getLogger
from urllib import response
from django.db import connection
from flask import *

# creating a Flask app
app = Flask(__name__)

# creating a logger
log = getLogger(__name__)

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
    conn = sqlite3.connect("dvdrent.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT app_dvd.title, app_dvd.year, app_author.full_name, app_genre.name, app_main_actor.name, app_main_actor.surname, app_main_actor.age, app_adult_restriction.adult_movie FROM app_dvd JOIN app_author ON app_dvd.author_id = app_author.id JOIN app_genre ON app_dvd.genre_id = app_genre.id JOIN app_main_actor ON app_dvd.main_actor_id = app_main_actor.id JOIN app_adult_restriction ON app_dvd.adult_restriction_id = app_adult_restriction.id"
    )
    rows = cur.fetchall()
    print("Get all dvd entries successfully")
    return render_template("get_dvd.html", rows=rows)


@app.route("/add_entry", methods=["POST"])
def add_entry():
    if request.method == "POST":
        try:
            title = request.form["title"]
            year = request.form["year"]
            author = request.form["author_id"]
            genre = request.form["genre_id"]
            main_actor = request.form["main_actor_id"]
            adult_restriction = request.form["adult_restriction_id"]

            with sqlite3.connect("dvdrent.db") as connection:
                cur = connection.cursor()
                cur.execute(
                    "INSERT INTO app_dvd (title, year, author_id, genre_id, main_actor_id, adult_restriction_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (title, year, author, genre, main_actor, adult_restriction),
                )
                connection.commit()
                print("Data inserted successfully")
                return render_template("added_sucess.html")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()


@app.route("/delete_dvd_entry", methods=["POST"])
def delete_dvd_entry():
    if request.method == "POST":
        print(f"{request.method} request received")
        try:
            title = request.form["title"]
            with sqlite3.connect("dvdrent.db") as connection:
                cur = connection.cursor()
                cur.execute("DELETE FROM app_dvd WHERE title = ?", (title,))
                connection.commit()
                print(f"{request.method} request processed")
                return render_template("delete_sucess.html")
        except:
            connection.rollback()
            print("Error while deleting record")
    else:
        return response("Method not allowed", status=405)


@app.route("/update_dvd_entry", methods=["POST"])
def update_dvd_entry():
    if request.method == "POST":
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
                    "UPDATE app_dvd SET year = ?, author_id = ?, genre_id = ?, main_actor_id = ?, adult_restriction_id = ? WHERE title = ?",
                    (year, author, genre, main_actor, adult_restriction, title),
                )
                connection.commit()
                return render_template("index.html")
        except Exception as e:
            print(f"Error occured {e}")
        finally:
            connection.close()


# download all data from database as csv file using pandas
@app.route("/download_data_in_csv", methods=["GET"])
def download_data_in_csv():
    try:
        conn = sqlite3.connect("dvdrent.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT app_dvd.title, app_dvd.year, app_author.full_name, app_genre.name, app_main_actor.name, app_main_actor.surname, app_main_actor.age, app_adult_restriction.adult_movie FROM app_dvd JOIN app_author ON app_dvd.author_id = app_author.id JOIN app_genre ON app_dvd.genre_id = app_genre.id JOIN app_main_actor ON app_dvd.main_actor_id = app_main_actor.id JOIN app_adult_restriction ON app_dvd.adult_restriction_id = app_adult_restriction.id"
        )
        rows = cur.fetchall()
        headers = [i[0] for i in cur.description]
        headers_upper = [i.upper() for i in headers]
        df = pd.DataFrame(rows, columns=headers_upper)
        print("Get all dvd entries successfully")
        df.to_csv("dvd_report.csv", index=False)
        return send_file("dvd_report.csv", as_attachment=True)
    except Exception as e:
        print(f"Error occured {e}")


# running the app
if __name__ == "__main__":
    app.run(debug=True)
