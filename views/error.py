from flask import Blueprint, render_template

error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="The page you are looking for is reenacting its disappearance!", error_code=404), 404

@error.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message="Something went wrong because my brain isn't braining, please try again later", error_code=500), 500

