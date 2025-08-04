from doctest import master
from flask import Blueprint, current_app, url_for
import pandas as pd
import os

bp = Blueprint('quiz', __name__, url_prefix='/quiz')

# === Endpoints === #

@bp.route('/', methods=['GET'])
def list_quizzes():
    return (f"List of quizzes", 200)

@bp.route('/<string:quiz_name>', methods=['GET'])
def get_quiz(quiz_name):
    return (f"Quiz: {quiz_name}", 200)

@bp.route('/submit_session', methods=['POST'])
def submit_session():
    return (f"Session submitted", 200)

@bp.route('/results', methods=['GET'])
def get_results():
    results = pd.read_excel(current_app.config['RESULTS_EXCEL_FILE'])
    results_html = results.to_html(header="true", index=False, na_rep='')
    return (results_html, 200)

@bp.route('/master_list', methods=['GET'])
def get_master_list():
    master_list = pd.read_excel(current_app.config['QUIZ_EXCEL_FILE'])
    master_list_html = master_list.to_html(header="true", index=False, na_rep='')
    return (master_list_html, 200)

# === Utility Functions === #
