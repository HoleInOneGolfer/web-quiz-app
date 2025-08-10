from flask import Blueprint, current_app, redirect, render_template, request, send_from_directory
import pandas as pd
import os

from .data import load_data, save_data

bp = Blueprint('quiz', __name__)

# === Endpoints === #

@bp.route('/data/<path:filename>', methods=['GET'])
def data(filename):
    return send_from_directory(current_app.config['DATA_DIR'], filename)

@bp.route('/list', methods=['GET'])
def list():
    quiz_data = load_data(current_app.config['QUIZ_DATA_FILE'])
    quiz_list = pd.unique(quiz_data['quiz_name']).tolist()
    return render_template('list.jinja', title="Quiz List", quiz_list=quiz_list)

@bp.route('/quiz/<quiz_name>', methods=['GET'])
def quiz(quiz_name):
    quiz_data = load_data(current_app.config['QUIZ_DATA_FILE'])
    quiz_data = quiz_data[quiz_data['quiz_name'] == quiz_name]
    quiz_data = quiz_data.to_dict(orient='records')

    return render_template('quiz.jinja', title=quiz_name, quiz_name=quiz_name, quiz_data=quiz_data)

@bp.route('/submit', methods=['POST'])
def submit():
    session_data = request.get_json()
    session_data = pd.DataFrame([session_data])

    save_data(session_data, current_app.config['RESULTS_DATA_FILE'])

    return {}, 200

@bp.route('/info', methods=['GET'])
def info():
    results = load_data(current_app.config['RESULTS_DATA_FILE'])
    results_html = results.to_html(header="true", index=False, na_rep='')

    quizzes = load_data(current_app.config['QUIZ_DATA_FILE'])
    quizzes_html = quizzes.to_html(header="true", index=False, na_rep='')

    html = {
        'Results': results_html,
        'Quizzes': quizzes_html
    }

    return render_template('info.jinja', title='Info', html=html)
