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
    randvid = random.choice(arr) #Selects a random video file from a folder with a path above and returns it
    return render_template('home.html', randvid=randvid)

@app.route('/routine/')
def all_routines():
    results = sqlite_conn('database.db', "SELECT * FROM Routine")
    description = sqlite_conn('database.db', "SELECT Routine.decscription from Routine")
    return render_template('routine.html', routines=results, description=description)

@app.route('/help/')
def help():
    results = sqlite_conn('database.db', "select id, name from Exercise where Exercise.id in (select exercise_id from Help)")
    return render_template('help.html', help_exercise=results)

@app.route('/workout_help/<int:id>')
def workouthelper(id):
    results = sqlite_conn('database.db', "SELECT desc FROM Help where Help.exercise_id == {}".format(id))
    return render_template('workout_help.html', results=results)
    
@app.route('/exercisenow/<int:id>')
def exercisenow(id):
    exercisenow = sqlite_conn('database.db', 'SELECT Exercise.name, ExerciseRoutine.reps, ExerciseRoutine.sets, ExerciseRoutine.term, Exercise.description FROM ExerciseRoutine INNER JOIN Exercise ON ExerciseRoutine.Exercise=Exercise.id WHERE ExerciseRoutine.Routine= (SELECT id FROM Routine WHERE id = {})'.format(id))
    description = sqlite_conn('database.db', 'SELECT Routine.decscription FROM Routine Where id == {};'.format(id), True)
    return render_template('exercisenow.html', exercisenow=exercisenow, description=description[0])

@app.route('/images_copyrights/')
def image_source():   
    return render_template("images_copyrights.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/testimonial/')
def testimonial():
    return render_template("testimonial.html")

if __name__ == '__main__':
    app.run(debug=True)
