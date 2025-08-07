""" Flask Error handling blueprint """

from flask import Blueprint, render_template

bp = Blueprint('error', __name__)

@bp.app_errorhandler(Exception)
def handle_exception(e):
    if not hasattr(e, 'code'):
        e.code = 500

    return render_template('error.jinja', title="Error", error_message=str(e)), e.code
