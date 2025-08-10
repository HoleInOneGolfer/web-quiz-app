from flask import Blueprint, current_app, render_template, request
import pandas as pd
import os

bp = Blueprint('quiz', __name__)

def load_data(file_path, create_if_missing=True):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    else:
        df = pd.DataFrame()
        if create_if_missing:
            df.to_csv(file_path, index=False)
        return df

def save_data(df, file_path):
    df.columns = df.columns.str.lower()

    file_df = load_data(file_path)

    if file_df.empty:
        file_df = pd.DataFrame(columns=df.columns)

    file_df = pd.concat([file_df, df], ignore_index=True)
    file_df.to_csv(file_path, index=False)

# === Endpoints === #

@bp.route('/', methods=['GET'])
def list_quizzes():
    quiz_data = load_data(current_app.config['QUIZ_DATA_FILE'])
    quiz_list = pd.unique(quiz_data['quiz_name']).tolist()
    return render_template('list.jinja', title="Quiz List", quiz_list=quiz_list)

@bp.route('/quiz/<quiz_name>', methods=['GET'])
def get_quiz(quiz_name):
    quiz_data = load_data(current_app.config['QUIZ_DATA_FILE'])
    quiz_data = quiz_data[quiz_data['quiz_name'] == quiz_name]
    quiz_data = quiz_data.to_dict(orient='records')

    return render_template('quiz.jinja', title=quiz_name, quiz_name=quiz_name, quiz_data=quiz_data)

@bp.route('/submit_session', methods=['POST'])
def submit_session():
    session_data = request.get_json()
    session_data = pd.DataFrame([session_data])

    save_data(session_data, current_app.config['RESULTS_DATA_FILE'])

    return {}, 200

@bp.route('/quiz_results', methods=['GET'])
def get_results():
    results = load_data(current_app.config['RESULTS_DATA_FILE'])
    results_html = results.to_html(header="true", index=False, na_rep='')
    return render_template('data.jinja', title='Quiz Results', data_html=results_html)

@bp.route('/quiz_data', methods=['GET'])
def get_data():
    quiz_data = load_data(current_app.config['QUIZ_DATA_FILE'])
    quiz_data_html = quiz_data.to_html(header="true", index=False, na_rep='')
    return render_template('data.jinja', title='Quiz Data', data_html=quiz_data_html)
