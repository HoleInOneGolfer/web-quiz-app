from flask import Blueprint

bp = Blueprint('debug', __name__, url_prefix='/debug')

@bp.route('/results', methods=['GET'])
def get_results():
    return ("Results endpoint", 200)

@bp.route('/quizzes', methods=['GET'])
def get_quizzes():
    return ("Quizzes endpoint", 200)
