from flask import Flask, render_template
import sqlite3
import os
import random


app = Flask(__name__)

@app.route('/')
def home():
    arr = os.listdir(r'C:\Users\brendan\12DTP\12DTP\NoExcuse\static\videos with inspirational qoutes')
    randvid = random.choice(arr)
    #codes
    return render_template('home.html', randvid=randvid)

@app.route('/routine/')
def all_routines():
    #codes
    return render_template('routine.html')

@app.route('/help/')
def help():
    #codes
    return render_template('help.html')

@app.route('/exercisenow/<int:id>')
def exercisenow(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT Exercise.name, ExerciseRoutine.reps, ExerciseRoutine.sets, ExerciseRoutine.term FROM ExerciseRoutine INNER JOIN Exercise ON ExerciseRoutine.Exercise=Exercise.id WHERE ExerciseRoutine.Routine= (SELECT id FROM Routine WHERE id = {})'.format(id))
    results = cur.fetchall()
    return render_template('exercisenow.html', exercisenow=results)

if __name__ == '__main__':
    app.run(debug=True)