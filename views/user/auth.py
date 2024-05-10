import requests
from flask import Blueprint, render_template, request, redirect, url_for, session

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        company = request.form['company']
        password = request.form['password']
        
        # Make API call to fetch company name and password
        try:
            api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            request_body_data = {
                "Action": "Find",
                "Properties": {
                    "Locale": "en-IN"
                },
                "Rows":[
                    {
                        "Name": company
                    }
                ]
            }
            headers = {"Content-Type":"application/json"}
            response = requests.post(api_url, json=request_body_data, headers=headers)
            [data] = response.json()
            
            # Check if the company exists and the password matches
            if response.status_code == 200 and data.get('pass') == password:
                # Set session variable to indicate user is authenticated
                session['logged_in'] = True
                session['company'] = company
                session['type'] = data['Type']
                session['ID'] = data['ID']
                return redirect(url_for('dash.dash_page'))
            else:
                error = "Invalid company name or password. Please try again."
        except Exception as e:
            error = "An error occurred while logging in. Please try again later."

    return render_template('user/auth.html', error=error)


@auth.route('/logout')
def logout():
    # Clear session data to logout the user
    session.clear()
    return redirect(url_for('auth.login_page'))
