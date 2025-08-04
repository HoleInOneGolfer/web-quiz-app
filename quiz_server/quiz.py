from flask import Blueprint

bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@bp.route('/', methods=['GET'])
def list_quizzes():
    return ("List of quizzes", 200)

@bp.route('/<quiz_name>', methods=['GET'])
def get_quiz(quiz_name):
    return (f"Quiz: {quiz_name}", 200)
