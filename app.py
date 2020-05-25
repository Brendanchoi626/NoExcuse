import os
import random
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    arr = os.listdir(r'C:\Users\brend\12DTP\12DTP\NoExcuse\static\videos with inspirational qoutes')
    randvid = random.choice(arr)
    #codes
    return render_template('home.html', randvid=randvid)

@app.route('/routine/')
def all_routines():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Routine;')
    routines = cur.fetchall()
    #codes 
    return render_template('routine.html', routines=routines)

@app.route('/help/')
def help():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM Exercise')
    help_exercise = cur.fetchall()
    #codes
    return render_template('help.html', help_exercise=help_exercise)

@app.route('/workouthelper/<int:id>')
def workouthelper():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute()
    
@app.route('/exercisenow/<int:id>')
def exercisenow(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT Exercise.name, ExerciseRoutine.reps, ExerciseRoutine.sets, ExerciseRoutine.term FROM ExerciseRoutine INNER JOIN Exercise ON ExerciseRoutine.Exercise=Exercise.id WHERE ExerciseRoutine.Routine= (SELECT id FROM Routine WHERE id = {});'.format(id))
    exercisenow = cur.fetchall()
    cur.execute("SELECT Routine.decscription FROM Routine Where id == {};".format(id))
    description = cur.fetchone()
    return render_template('exercisenow.html', exercisenow=exercisenow, description=description[0])

@app.route('/images_copyrights/')
def image_source():
    return render_template("images_copyrights.html")

if __name__ == '__main__':
    app.run(debug=True)
