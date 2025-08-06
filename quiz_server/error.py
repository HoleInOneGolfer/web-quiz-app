""" Flask Error handling blueprint """

from flask import Blueprint, render_template

bp = Blueprint('error', __name__)

# handler for all Exceptions
@bp.app_errorhandler(Exception)
def handle_exception(e):
    return render_template('error.jinja', title="Error", error_message=str(e)), 500
