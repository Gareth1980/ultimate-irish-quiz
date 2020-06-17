import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

from os import path
if path.exists("env.py"):
    import env 

MONGO_URI = os.environ.get("MONGO_URI") 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'quiz_questions'
app.config["MONGO_URI"] = MONGO_URI


mongo = PyMongo(app)

@app.route('/')
@app.route('/get_questions')
def get_questions():
    return render_template("question_and_answer.html", question_and_answer=mongo.db.question_and_answer.find())

@app.route('/add_question')
def add_question():
    return render_template('addquestion.html', categories=mongo.db.categories.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)