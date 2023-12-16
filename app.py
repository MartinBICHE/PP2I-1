from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
import sqlite3

# Initialisation
app = Flask(__name__)
app.config['SECRET_KEY'] = "MySuperSecretKey"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Connection à la base de données
def db_connection():
    conn = sqlite3.connect('codesafe.db')
    return conn

# Classe utilisateur
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def id(self):
        return self.username

    @staticmethod
    def get_user_by_username(username):
        conn = db_connection()
        user_data = conn.execute('''
            SELECT * FROM users WHERE username=?''',
            (username,)).fetchone()
        conn.close()
        if user_data:
            return User(user_data[0], user_data[1])
        return None

# User loader
@login_manager.user_loader
def load_user(username):
    return User.get_user_by_username(username)

@app.route('/')
def index():
    return 'Index'

# Register
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = db_connection()
        try:
            conn.execute('''
                INSERT INTO users
                VALUES (?, ?)''',
                (username, hashed_password))
        except sqlite3.IntegrityError:
            return render_template('register.html', usernameExists=True)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('register.html')

# Login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user_by_username(username)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', badCredentials=True)
    return render_template('login.html', badCredentials=False)

# Logout
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/quizz/')
def quizz():
    return 'Quizz'

@app.route('/resultats/')
def resultats():
    return 'Resultats'