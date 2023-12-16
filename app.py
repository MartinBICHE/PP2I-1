from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/register/')
def register():
    return 'Register'

@app.route('/login/')
def login():
    return 'Login'

@app.route('/quizz/')
def quizz():
    questions = [
        ["Question 1", ["Réponse 1.1", "Réponse 1.2", "Réponse 1.3", "Réponse 1.4"]],
        ["Question 2", ["Réponse 2.1", "Réponse 2.2", "Réponse 2.3", "Réponse 2.4"]],
        ["Question 3", ["Réponse 3.1", "Réponse 3.2", "Réponse 3.3", "Réponse 3.4"]],
        ["Question 4", ["Réponse 4.1", "Réponse 4.2", "Réponse 4.3", "Réponse 4.4"]],
    ]
    return render_template('quizz.html',questions=questions)

@app.route('/resultats/')
def resultats():
    return 'Resultats'