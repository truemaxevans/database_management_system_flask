# importing necessary libraries
from logging import getLogger
from urllib import response
from django.db import connection
from flask import *

import sqlite3

# creating a Flask app
app = Flask(__name__)

# creating a logger
log = getLogger(__name__)

# rendering html templates and static files with url
@app.route('/')
def index():
    return render_template('index.html');


@app.route('/add_dvd')
def add_dvd():
    return render_template('add_dvd.html');


@app.route('/get_dvd')
def get_dvd():
    return render_template('get_dvd.html');

@app.route('/delete_dvd')
def delete_dvd():
    return render_template('delete_dvd.html');

@app.route('/update_dvd')
def update_dvd():
    return render_template('update_dvd.html');

# @app.route('/download_all_csv')
# def download_all_csv():
#     return render_template('download_all_csv.html');

# run SQL execution in functions and return results
@app.route('/get_dvd_entries', methods=['GET'])
def get_all_dvd():
    conn = sqlite3.connect('dvdrent.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT app_dvd.title, app_author.full_name, app_genre.name, app_main_actor.name, app_main_actor.surname, app_main_actor.age, app_adult_restriction.adult_movie FROM app_dvd JOIN app_author ON app_dvd.author_id = app_author.id JOIN app_genre ON app_dvd.genre_id = app_genre.id JOIN app_main_actor ON app_dvd.main_actor_id = app_main_actor.id JOIN app_adult_restriction ON app_dvd.adult_restriction_id = app_adult_restriction.id")
    rows = cur.fetchall()
    return render_template('get_dvd.html', rows=rows)
    

@app.route('/add_entry', methods=['POST'])
def add_entry():
    if request.method == 'POST':
        log.info(f'{request.method} request received')
        try:
            title = request.form['title']
            author = request.form['author']
            year = request.form['year']
            genre = request.form['genre']
            main_actor = request.form['main_actors']
            adult_restriction = request.form['adult_restriction']

            with sqlite3.connect("dvdrent.db") as connection:
                cur = connection.cursor()
                cur.execute("INSERT INTO dvd_discs (title, author, year, genre, main_actor) VALUES (?,?,?,?,?)", (title, author, year, genre, main_actor))
                connection.commit()
                log.info(f'{request.method} request processed')
            return render_template('add_dvd.html')
        except:
            log.info(f'{request.method} request failed')
            return render_template('add_dvd.html')
    else:
        return response('Method not allowedd', status=405)


@app.route('/delete_dvd_entry', methods=['POST'])
def delete_dvd_entry():
    if request.method == 'POST':
        log.info(f'{request.method} request received')
        try:
            title = request.form['title']
            with sqlite3.connect("dvdrent.db") as connection:
                cur = connection.cursor()
                cur.execute("DELETE FROM app_dvd WHERE title = ?", (title,))
                connection.commit()
                log.info(f'{request.method} request processed')
                return render_template('sucess.html')
        except:
            connection.rollback()
            log.error('Error while deleting record')
        
    else:
        return response('Method not allowed', status=405)


@app.route('/update_dvd_entry', methods=['PATCH'])
def update_dvd_entry():
    if request.method == 'PATCH':
        log.info(f'{request.method} request received')
        try:
            title = request.form['title']
            author = request.form['author']
            year = request.form['year']
            genre = request.form['genre']
            main_actor = request.form['main_actors']
            adult_restriction = request.form['adult_restriction']

            with sqlite3.connect("dvdrent.db") as connection:
                cur = connection.cursor()
                cur.execute("UPDATE dvd_dics SET author = ?, year = ?, genre = ?, main_actor = ? WHERE title = ?", (author, year, genre, main_actor, title))
                connection.commit()
                log.info(f'{request.method} request processed')
        except:
            connection.rollback()
            log.error('Error while updating record')
    else:
        return response('Method not allowed', status=405)

# @app.route('/download_all_csv', methods=['GET'])
# def download_all_csv():
#     if request.method == 'GET':
#         try:
#             conn = sqlite3.connect('dvdrent.db')
#             conn.row_factory = sqlite3.Row
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM dvd")
#             rows = cur.fetchall()
#             return render_template('dvd.csv', rows=rows)
#         except Exception as e:
#             return Exception(e)

# running the app
if __name__ == "__main__":
    app.run(debug = True)  
