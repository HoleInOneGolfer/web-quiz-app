import os
from flask import Flask, render_template, request

from data_manager import *

QUIZ_EXCEL_FILE = os.path.join(os.getcwd(), 'data', 'quizzes.xlsx')
RESULTS_EXCEL_FILE = os.path.join(os.getcwd(), 'data', 'results.xlsx')
print(QUIZ_EXCEL_FILE, RESULTS_EXCEL_FILE)

QUIZ_DF = load_excel_data(QUIZ_EXCEL_FILE)


app = Flask(__name__)

@app.route('/')
def index():
    quizzes = extract_unique_values_and_clean(QUIZ_DF, 'quiz_name')
    return render_template('list.html.jinja', quizzes=quizzes, title='Quiz List')

@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):

    quiz_data_dict = get_quiz_data_dict(QUIZ_DF, quiz_name)
    quiz_data_dataframe = get_quiz_data_dataframe(QUIZ_DF, quiz_name)
    quiz_data_json = get_quiz_data_json(QUIZ_DF, quiz_name)
    quiz_unique_bg_images = extract_unique_values_and_clean(quiz_data_dataframe, 'bg_image')
    quiz_unique_hint_images = extract_unique_values_and_clean(quiz_data_dataframe, 'hint_image')


    return render_template('quiz.html.jinja',
                           title=quiz_name,
                           quiz_data_dict= quiz_data_dict,
                           quiz_data_dataframe=quiz_data_dataframe,
                           quiz_data_json=quiz_data_json,
                           quiz_unique_bg_images=quiz_unique_bg_images,
                           quiz_unique_hint_images=quiz_unique_hint_images)

# post route that handles the quiz submission and saves the results to results.xlsx
@app.route('/send_score', methods=['POST'])
def send_score():
    if request.method == 'POST':

        data = request.get_json()['SESSION']
        df = pd.DataFrame([data])
        results_df = load_excel_data(RESULTS_EXCEL_FILE)

        df.columns = df.columns.str.lower()

        # change start_time, end_time, and total_time to datetime format
        df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
        df['end_time'] = pd.to_datetime(df['end_time'], unit='ms')

        results_df = pd.concat([results_df, df], ignore_index=True)
        results_df.to_excel(RESULTS_EXCEL_FILE, index=False)

    return {'status': 'success', 'message': 'Score received successfully.'}, 200

# route that shows the results from the results.xlsx file as a table
@app.route('/results')
def results():
    results_df = load_excel_data(RESULTS_EXCEL_FILE)
    if results_df.empty:
        return render_template('results.html.jinja', title='Results', results='No results found.')

    results_html = df_to_html(results_df)
    print(results_html)
    return render_template('results.html.jinja', title='Results', results_html=results_html)

@app.route('/tests')
def tests_misc():
    quizzes = extract_unique_values_and_clean(QUIZ_DF, 'quiz_name')
    questions = extract_unique_values_and_clean(QUIZ_DF, 'question_text')
    answers = extract_unique_values_and_clean(QUIZ_DF, ['answer_1', 'answer_2', 'answer_3', 'answer_4'])
    hints = extract_unique_values_and_clean(QUIZ_DF, 'hint')
    df_html = df_to_html(QUIZ_DF)

    return render_template('tests.html.jinja', title="Tests", quizzes=quizzes, questions=questions, answers=answers, hints=hints, df_html=df_html)

# ========================= #

# === Debug Endpoints === #
@app.route('/debug/', methods=['GET'])
def debug():
    return {}, 200

@app.route('/debug/results', methods=['GET'])
def debug_results():
    return {}, 200

@app.route('/debug/quizzes', methods=['GET'])
def debug_quizzes():
    return {}, 200

# === Error Endpoints === #
@app.errorhandler(Exception)
def handle_exception(e):
    error_info = {
        'status': str(e),
        'stack': e.__traceback__
    }
    # Log the error information for debugging
    app.logger.error(f"An error occurred: {error_info['status']}", exc_info=e)

    return render_template('error.html.jinja', error=error_info, title='Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
