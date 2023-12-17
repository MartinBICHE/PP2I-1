from flask import Flask, render_template, request
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
    cursor = conn.execute(f'SELECT question_txt FROM questions WHERE id_categorie={categorie}')
    qs = cursor.fetchall()
    questions = [item[0] for item in qs]
  
    current_question = questions[question_index] if question_index < len(questions) else None

    cursor1 = conn.execute(f'SELECT id_question FROM questions WHERE id_categorie={categorie}')
    id = cursor1.fetchone()[0]

    cursor2 = conn.execute(f'SELECT reponse_txt FROM reponses WHERE id_question={id}')
    all_ans = cursor2.fetchall()
    all_answers = [item[0] for item in all_ans]

    cursor3 = conn.execute(f'SELECT reponse_txt FROM reponses WHERE id_question={id} AND is_good=1')
    good = cursor3.fetchall()
    correct_answer = [item[0] for item in good][0]
    conn.close()

    if request.method == 'POST':
        user_response = request.form.get('reponse')
        is_correct = user_response == correct_answer
        return render_template('quizz.html', current_question=current_question,
                               question_index=question_index, user_response=user_response,
                               is_correct=is_correct, categorie=categorie,
                               all_answers=all_answers, correct_answer=correct_answer)
    else:
        return render_template('quizz.html', current_question=current_question, 
                               question_index=question_index, categorie=categorie,
                               all_answers=all_answers)


@app.route('/resultats/')
def resultats():
    return 'Resultats'


if __name__ == '__main__':
    app.run(debug=True)
    