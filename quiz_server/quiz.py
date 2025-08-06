from flask import Blueprint, current_app, render_template, request, session
import pandas as pd
import os

bp = Blueprint('quiz', __name__)

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        df = pd.DataFrame()
        df.to_excel(file_path, index=False)
        return df


# === Endpoints === #

@bp.route('/', methods=['GET'])
def list_quizzes():
    quiz_data = load_data(current_app.config['QUIZ_EXCEL_FILE'])
    quiz_list = pd.unique(quiz_data['quiz_name']).tolist()
    return render_template('list.jinja', title="Quiz List", quiz_list=quiz_list)

@bp.route('/quiz/<quiz_name>', methods=['GET'])
def get_quiz(quiz_name):
    quiz_data = load_data(current_app.config['QUIZ_EXCEL_FILE'])
    quiz_data = quiz_data[quiz_data['quiz_name'] == quiz_name]
    quiz_data = quiz_data.to_dict(orient='records')
    return  render_template('quiz.jinja', title=quiz_name, quiz_name=quiz_name, quiz_data=quiz_data)

@bp.route('/submit_session', methods=['POST'])
def submit_session():
    session_data = request.get_json()
    session_data = pd.DataFrame([session_data])
    session_data.columns = session_data.columns.str.lower()

    results = load_data(current_app.config['RESULTS_EXCEL_FILE'])

    results = pd.concat([results, session_data], ignore_index=True)
    results.to_excel(current_app.config['RESULTS_EXCEL_FILE'], index=False)


    return (f"Session submitted", 200)

@bp.route('/quiz_results', methods=['GET'])
def get_results():
    results = load_data(current_app.config['RESULTS_EXCEL_FILE'])
    results_html = results.to_html(header="true", index=False, na_rep='')
    return render_template('data.jinja', title='Quiz Results', data_html=results_html)

@bp.route('/quiz_data', methods=['GET'])
def get_master_list():
    quiz_data = load_data(current_app.config['QUIZ_EXCEL_FILE'])
    quiz_data_html = quiz_data.to_html(header="true", index=False, na_rep='')
    return render_template('data.jinja', title='Quiz Data', data_html=quiz_data_html)
