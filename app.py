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

@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    # Si l'utilisateur veut afficher la page
    if request.method == 'GET':
        conn = db_connection()
        # On récupère les ids de toutes les catégories
        all_categories = conn.execute('''
            SELECT id_categorie, nom_categorie FROM categories''').fetchall()
        all_categories = [list(id_cat) for id_cat in all_categories]
        # On récupère les résultats de l'utilisateur dans chaque catégorie
        data = []
        for id_cat, nom_cat in all_categories:
            pourcent = conn.execute('''
                SELECT pourcent FROM pourcent_categorie
                WHERE id_categorie=? AND username=?''',
                (id_cat, nom_cat)).fetchone()
            if pourcent != None:
                data.append([nom_cat, pourcent])
            else:
                data.append([nom_cat, 0])
        conn.close()
        # On affiche la page
        return render_template('profile.html', username=current_user.username,
                            data=data)
    # Si l'utilisateur veut changer de mot de passe
    else:
        old_password = request.form['old-password']
        new_password1 = request.form['new-password1']
        new_password2 = request.form['new-password2']
        user = User.get_user_by_username(current_user.username)
        if (user and bcrypt.check_password_hash(user.password, old_password)
            and new_password1 == new_password2):
            # Le mot de passe est changé
            hashed_password = bcrypt.generate_password_hash(new_password1).decode('utf-8')
            conn = db_connection()
            conn.execute('''
                UPDATE users
                SET password=?
                WHERE username=?''',
                (hashed_password, current_user.username))
            conn.commit()
            conn.close()
            logout_user()
            return redirect('/login/')
        elif user and bcrypt.check_password_hash(user.password, old_password):
            # Les deux nouveaux mots de passe ne sont pas les mêmes
            # On doit récupérer les résultats pour les réafficher
            conn = db_connection()
            # On récupère les ids de toutes les catégories
            all_categories = conn.execute('''
                SELECT id_categorie, nom_categorie FROM categories''').fetchall()
            all_categories = [list(id_cat) for id_cat in all_categories]
            # On récupère les résultats de l'utilisateur dans chaque catégorie
            data = []
            for id_cat, nom_cat in all_categories:
                pourcent = conn.execute('''
                    SELECT pourcent FROM pourcent_categorie
                    WHERE id_categorie=? AND username=?''',
                    (id_cat, nom_cat)).fetchone()
                if pourcent != None:
                    data.append([nom_cat, pourcent])
                else:
                    data.append([nom_cat, 0])
            conn.close()
            return render_template('profile.html', username=current_user.username,
                                   data=data, differentNewPasswords=True)
        else:
            # Le mot de passe actuel entré ne correspond pas à celui de la BD
            # On doit récupérer les résultats pour les réafficher
            conn = db_connection()
            # On récupère les ids de toutes les catégories
            all_categories = conn.execute('''
                SELECT id_categorie, nom_categorie FROM categories''').fetchall()
            all_categories = [list(id_cat) for id_cat in all_categories]
            # On récupère les résultats de l'utilisateur dans chaque catégorie
            data = []
            for id_cat, nom_cat in all_categories:
                pourcent = conn.execute('''
                    SELECT pourcent FROM pourcent_categorie
                    WHERE id_categorie=? AND username=?''',
                    (id_cat, nom_cat)).fetchone()
                if pourcent != None:
                    data.append([nom_cat, pourcent])
                else:
                    data.append([nom_cat, 0])
            conn.close()
            return render_template('profile.html', username=current_user.username,
                                   data=data, badOldPassword=True)