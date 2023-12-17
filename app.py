from flask import Flask, render_template, request, session , redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def db_connection():
    conn = sqlite3.connect('codesafe.db')
    return conn


@app.route('/')
def index():
    return 'Index'


@app.route('/register/')
def register():
    return 'Register'


@app.route('/login/')
def login():
    return 'Login'


@app.route('/quizz/<categorie>', methods=['GET','POST'])
def quizz(categorie): 
    try:
        question_index = int(request.args.get('question_index'))

    except TypeError:
        question_index = 0

    conn = db_connection()

    question_data = conn.execute('''
        SELECT id_question, question_txt
        FROM questions
        WHERE id_categorie=?''',
        (categorie,)).fetchall()

    # on met toutes les informations dans une liste de listes res :
    # [ ['question1', ['réponse1', 'réponse2', ...], 'réponse juste'], ['question2', ...], ... ]
    res = []
    for question in question_data:
        reponses = conn.execute('''
            SELECT reponse_txt
            FROM reponses
            WHERE id_question = ?''',
            (question[0],)).fetchall()
        list_reponses = [reponse[0] for reponse in reponses]
        bonne_reponse = conn.execute('''
            SELECT reponse_txt
            FROM reponses
            WHERE id_question = ? AND is_good = 1''',
            (question[0],)).fetchone()[0]
        res.append([question[1], list_reponses, bonne_reponse])

    current_question = res[question_index] if question_index < len(res) else None

    if request.method == 'POST':
        user_response = request.form.get('reponse')
        is_correct = user_response == current_question[2]
        return render_template('quizz.html', current_question=current_question,
                               question_index=question_index, user_response=user_response,
                               is_correct=is_correct, categorie=categorie)
    else:
        return render_template('quizz.html', current_question=current_question, 
                               question_index=question_index, categorie=categorie)
    

@app.route('/resultats/')
def resultats():
    return 'Resultats'


if __name__ == '__main__':
    app.run(debug=True)
    