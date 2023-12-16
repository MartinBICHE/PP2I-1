from flask import *
app = Flask(__name__)

@app.route('/')
def index():
    liste = ['a','b','c','d','e','f','g','mots de passe','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    return render_template('index.html',bd = liste)

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