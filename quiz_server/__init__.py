import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
        QUIZ_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'quiz.csv'),
        RESULTS_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'results.csv'),
    )

    from . import quiz
    app.register_blueprint(quiz.bp)

    return app
