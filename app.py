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

# Route for Home Page
@app.route('/')
@app.route('/get_questions')
def get_questions():
    return render_template("question_and_answer.html", question_and_answer=mongo.db.question_and_answer.find())

# Route to Add a Question
@app.route('/add_question')
def add_question():
    return render_template('addquestion.html', categories=mongo.db.categories.find())

# Route to Insert Question
@app.route('/insert_question', methods=['POST'])
def insert_question():
    question_and_answer = mongo.db.question_and_answer
    question_and_answer.insert_one(request.form.to_dict())
    return redirect(url_for('get_questions'))

# Route to Edit Question
@app.route('/edit_question/<question_and_answer_id>')
def edit_question(question_and_answer_id):
    the_question = mongo.db.question_and_answer.find_one(
        {"_id": ObjectId(question_and_answer_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editquestion.html', question_and_answer=the_question,
                           categories=all_categories)

# Route to Update Question 
@app.route('/update_question/<question_and_answer_id>', methods=['POST'])
def update_question(question_and_answer_id):
    question_and_answer = mongo.db.question_and_answer
    question_and_answer.update({'_id': ObjectId(question_and_answer_id)},
                               {
        'category_name': request.form.get('category_name'),
        'question': request.form.get('question'),
        'answer': request.form.get('answer')
    })
    return redirect(url_for('get_questions'))

# Route to Delete Question
@app.route('/delete_question/<question_and_answer_id>')
def delete_question(question_and_answer_id):
    mongo.db.question_and_answer.remove(
        {'_id': ObjectId(question_and_answer_id)})
    return redirect(url_for('get_questions'))

# Route for Shop Link
@app.route('/shop')
def get_shop():
    return render_template("shop.html")

# Route for Under Construction Link
@app.route('/under_construction')
def get_under_construction():
    return render_template("under_construction.html")

# Route for General Knowledge category
@app.route('/get_general_knowledge')
def get_general_knowledge():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'General Knowledge'}))

# Route for Geography category


@app.route('/get_geography')
def get_geography():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'Geography'}))

# Route for History category
@app.route('/get_history')
def get_history():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'History'}))

# Route for Music category
@app.route('/get_music')
def get_music():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'Music'}))

# Route for Politics category
@app.route('/get_politics')
def get_politics():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'Politics'}))

# Route for Sports category
@app.route('/get_sport')
def get_sport():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'Sport'}))

# Route for TV and Film category
@app.route('/get_tv_and_film')
def get_tv_and_film():
    return render_template("categories.html",
                           category=mongo.db.question_and_answer.find({'category_name': 'TV and Film'}))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
