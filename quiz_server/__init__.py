import os

from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
        QUIZ_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'quiz.csv'),
        RESULTS_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'results.csv'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import quiz
    app.register_blueprint(quiz.bp)

    from . import error
    app.register_blueprint(error.bp)

    return app
