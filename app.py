import os
import random
import sqlite3
from flask import Flask, render_template
from flask import abort

# Acts like a sql query runner
def sqlite_conn(database, query, single=False):
    "connects to a database and returns data"
    conn = sqlite3.connect(database)
    cur = conn.cursor() 
    cur.execute(query) 
    results = cur.fetchone() if single else cur.fetchall() 
    conn.close() 
    return results 

app = Flask(__name__)

# Routes for.... 
# homepage
@app.route('/')
def home():
    arr = os.listdir(r'C:\Users\brend\12DTP\12DTP\NoExcuse\static\videos with inspirational qoutes')
    randvid = random.choice(arr) #Selects a random video file from a folder with a path above and returns it
    return render_template('home.html', randvid=randvid)

# routine page
@app.route('/routine/')
def all_routines():
    results = sqlite_conn('database.db', "SELECT * FROM Routine")
    return render_template('routine.html', routines=results)

# help page
@app.route('/help/')
def help():
    results = sqlite_conn('database.db', "select id, name from Exercise where Exercise.id in (select exercise_id from Help)")
    return render_template('help.html', help=results)

# workout_help page
@app.route('/workout_help/<int:id>')
def workouthelper(id):
    results = sqlite_conn('database.db', "SELECT desc FROM Help where Help.exercise_id == {}".format(id))
    if results != []:
        return render_template('workout_help.html', results=results)
    else:  #if a person tries to get an information that isn't in the database through url, error 404 page is shown 
        abort(404)

# exercisenow page 
@app.route('/exercisenow/<int:id>')
def exercisenow(id):
    exercisenow = sqlite_conn('database.db', 'SELECT Exercise.name, Exercise.description FROM ExerciseRoutine INNER JOIN Exercise ON ExerciseRoutine.Exercise=Exercise.id WHERE ExerciseRoutine.Routine= (SELECT id FROM Routine WHERE id = {})'.format(id))
    description = sqlite_conn('database.db', 'SELECT Routine.description FROM Routine WHERE id == {};'.format(id), True)
    if exercisenow != [] and description != None:
        return render_template('exercisenow.html', exercisenow=exercisenow, description=description[0])
    else: #if a person tries to get an information that isn't in the database through url, error 404 page is shown 
        abort(404)

# image copyright page
@app.route('/images_copyrights/')
def image_source():   
    return render_template("images_copyrights.html")

# about page
@app.route('/about/')
def about():
    return render_template("about.html")

# testimpnial page
@app.route('/testimonial/')
def testimonial():
    return render_template("testimonial.html")
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
if __name__ == '__main__':
    app.run(debug=True)