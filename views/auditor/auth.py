import requests
from flask import Blueprint, render_template, request, redirect, url_for, session

auditor_auth = Blueprint('auditor_auth', __name__)


@auditor_auth.route('/auditor/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        auditor = request.form['auditor']
        password = request.form['password']
        
        # Make API call to fetch auditor name and password
        try:
            api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Auditors/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            request_body_data = {
                "Action": "Find",
                "Properties": {
                    "Locale": "en-IN"
                },
                "Rows":[
                    {
                        "Phone": auditor
                    }
                ]
            }
            headers = {"Content-Type":"application/json"}
            response = requests.post(api_url, json=request_body_data, headers=headers)
            [data] = response.json()
            
            # Check if the auditor exists and the password matches
            if response.status_code == 200 and data.get('Password') == password:
                # Set session variable to indicate user is authenticated
                session['auditor_logged_in'] = True
                return redirect(url_for('auditor_dash.dash_page'))
            else:
                error = "Invalid auditor name or password. Please try again."
        except Exception as e:
            error = "An error occurred while logging in. Please try again later."

    return render_template('auditor/auth.html', error=error)


@auditor_auth.route('/logout')
def logout():
    # Clear session data to logout the user
    # session.clear()
    session['auditor_logged_in'] = False
    return redirect(url_for('auditor_auth.login_page'))
