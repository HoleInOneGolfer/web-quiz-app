import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
        QUIZ_EXCEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'quiz.xlsx'),
        RESULTS_EXCEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'results.xlsx'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import quiz

    app.register_blueprint(quiz.bp)

    return app
