from flask import *
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/')
def register():
    return 'Register'

@app.route('/login/')
def login():
    return 'Login'

@app.route('/quizz/')
def quizz():
    return 'Quizz'

@app.route('/resultats/')
def resultats():
    return 'Resultats'