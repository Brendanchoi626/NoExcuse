import os
import random
import sqlite3
from flask import Flask, render_template

def sqlite_conn(database, query, single=False):
    "connects to a database and returns data"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchone() if single else cur.fetchall()
    conn.close()
    return results

app = Flask(__name__)


@app.route('/')
def home():
    arr = os.listdir(r'C:\Users\brend\12DTP\12DTP\NoExcuse\static\videos with inspirational qoutes')
    randvid = random.choice(arr)
    return render_template('home.html', randvid=randvid)

@app.route('/routine/')
def all_routines():
    results = sqlite_conn('database.db', "SELECT * FROM Routine")
    return render_template('routine.html', routines=results)

@app.route('/help/')
def help():
    results = sqlite_conn('database.db', "SELECT id, name FROM Exercise")
    return render_template('help.html', help_exercise=results)

@app.route('/workouthelper/<int:id>')
def workouthelper():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute()
    
@app.route('/exercisenow/<int:id>')
def exercisenow(id):
    exercisenow = sqlite_conn('database.db', 'SELECT Exercise.name, ExerciseRoutine.reps, ExerciseRoutine.sets, ExerciseRoutine.term FROM ExerciseRoutine INNER JOIN Exercise ON ExerciseRoutine.Exercise=Exercise.id WHERE ExerciseRoutine.Routine= (SELECT id FROM Routine WHERE id = {});'.format(id))
    description = sqlite_conn('database.db', 'SELECT Routine.decscription FROM Routine Where id == {};'.format(id), True)
    return render_template('exercisenow.html', exercisenow=exercisenow, description=description[0])

@app.route('/images_copyrights/')
def image_source():
    return render_template("images_copyrights.html")

if __name__ == '__main__':
    app.run(debug=True)
