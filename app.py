from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return 'Index'


@app.route('/register/')
def register():
    return 'Register'


@app.route('/login/')
def login():
    return 'Login'


@app.route('/quizz/', methods=['GET','POST'])
def quizz():
    questions = [
        ["Question 1", ["Réponse 1.1", "Réponse 1.2", "Réponse 1.3", "Réponse 1.4"], "Réponse 1.2"],
        ["Question 2", ["Réponse 2.1", "Réponse 2.2", "Réponse 2.3", "Réponse 2.4"], "Réponse 2.3"],
        ["Question 3", ["Réponse 3.1", "Réponse 3.2", "Réponse 3.3", "Réponse 3.4"], "Réponse 3.1"],
        ["Question 4", ["Réponse 4.1", "Réponse 4.2", "Réponse 4.3", "Réponse 4.4"], "Réponse 4.4"],
    ]
    try:
        question_index = int(request.args.get('question_index'))
    except TypeError:
        question_index = 0
    current_question = questions[question_index] if question_index < len(questions) else None
    if request.method == 'POST':
        user_response = request.form.get('reponse')
        correct_answer = current_question[2]
        print(user_response, correct_answer)
        is_correct = user_response == correct_answer
        return render_template('quizz.html', current_question=current_question,
                               question_index=question_index, user_response=user_response,
                               is_correct=is_correct)
    else:
        return render_template('quizz.html', current_question=current_question, question_index=question_index)


@app.route('/resultats/')
def resultats():
    return 'Resultats'


if __name__ == '__main__':
    app.run(debug=True)
    