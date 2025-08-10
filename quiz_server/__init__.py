import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['DATA_DIR'] = os.path.join(os.getcwd(), 'data')
    app.config['QUIZ_DATA_FILE'] = os.path.join(app.config['DATA_DIR'], 'quiz.csv')
    app.config['RESULTS_DATA_FILE'] = os.path.join(app.config['DATA_DIR'], 'results.csv')

    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    if not os.path.exists(app.config['QUIZ_DATA_FILE']):
        with open(app.config['QUIZ_DATA_FILE'], 'w') as f:
            f.write('quiz_name,question_number,question_text,answer_1,answer_2,answer_3,answer_4,answer_1_correct,answer_2_correct,answer_3_correct,answer_4_correct,hint,hint_image,bg_image,logo_image\n')

    from . import quiz
    app.register_blueprint(quiz.bp)

    app.add_url_rule('/', endpoint='quiz.list')


    return app
