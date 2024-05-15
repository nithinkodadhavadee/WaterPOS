from flask import Flask
from views.user.auth import auth
from views.user.dash import dash
from views.error import error
from views.auditor.auth import auditor_auth
from views.auditor.dash import auditor_dash
from views.auditor.waterMatrix import auditor_matrix
from views.auditor.companies import companies
from views.auditor.waterConservation import conservation
from views.auditor.report import report
from views.auditor.waterBalanceDiagram import auditor_balance_diagram

app = Flask(__name__, template_folder='./templates')

# Set a secret key for the session
app.secret_key = 'thisIsMySecretKey'

# Set session cookie expiration time to 10 minutes (600 seconds)
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(dash)
app.register_blueprint(error)
app.register_blueprint(auditor_auth)
app.register_blueprint(auditor_dash)
app.register_blueprint(auditor_matrix)
app.register_blueprint(companies)
app.register_blueprint(conservation)
app.register_blueprint(report)
app.register_blueprint(auditor_balance_diagram)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
