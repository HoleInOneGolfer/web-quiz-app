import os

from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config['DATA_DIR'] = os.path.join(os.getcwd(), 'data')
    app.config['QUIZ_DATA_FILE'] = os.path.join(app.config['DATA_DIR'], 'quiz.csv')
    app.config['RESULTS_DATA_FILE'] = os.path.join(app.config['DATA_DIR'], 'results.csv')

    os.makedirs(app.config['DATA_DIR'], exist_ok=True)

    from . import quiz
    app.register_blueprint(quiz.bp)

    app.add_url_rule('/', endpoint='quiz.list')


    return app
