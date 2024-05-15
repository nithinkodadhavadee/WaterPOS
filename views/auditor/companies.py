import requests
from flask import Blueprint, render_template, request, redirect, url_for, session
import time    
from ..generateFormView import generate_html_form

companies = Blueprint('companies', __name__)


# @companies.route('/auditor/login', methods=['GET', 'POST'])
# def login_page():
#     error = None
#     if request.method == 'POST':
#         auditor = request.form['auditor']
#         password = request.form['password']
        
#         # Make API call to fetch auditor name and password
#         try:
#             api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
#             request_body_data = {
#                 "Action": "Find",
#                 "Properties": {
#                     "Locale": "en-IN"
#                 },
#                 "Rows":[
#                     {
#                         "Name": auditor
#                     }
#                 ]
#             }
#             headers = {"Content-Type":"application/json"}
#             response = requests.post(api_url, json=request_body_data, headers=headers)
#             [data] = response.json()
            
#             # Check if the auditor exists and the password matches
#             if response.status_code == 200 and data.get('pass') == password:
#                 # Set session variable to indicate user is authenticated
#                 session['auditor_logged_in'] = True
#                 return redirect(url_for('auditor_dash.dash_page'))
#             else:
#                 error = "Invalid auditor name or password. Please try again."
#         except Exception as e:
#             error = "An error occurred while logging in. Please try again later."

#     return render_template('auditor/auth.html', error=error)


@companies.route('/auditor/create-company', methods=['GET', 'POST'])
def companie_form():
    if 'auditor_logged_in' in session:
        if request.method == "GET":
            form_view = "Cannot access the forms"
            companies_html = "Cannot access Companies"

            companies_form_api = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
            request_body = {
                    "Action": "Find",
                    "Properties": {
                        "Locale": "en-IN"
                    },
                    "Rows":[]
                }
            headers = {"Content-Type":"application/json"}
            companies_response = requests.post(companies_form_api, json=request_body, headers=headers)
        
            if companies_response.status_code == 200:
                # print(companies_response.json()[1:])
                companies_html = generate_html_form(companies_response.json()[1:], submit_link="/auditor/create-company")

        
            # Render the dashboard template with the company name and type
            return render_template('formPage.html', form_html=companies_html, submit_link = "/create-company")
        elif request.method == "POST":
            # Handle form submission
            form_data = request.form
            
            form_data = form_data.to_dict()
            form_entry = {
                "ID": int(time.time()),
                "Name": form_data.get('3', ""),
                "Type": form_data.get('4', "Automobile"),
                "Scope Of Work": form_data.get('5', ""),
                "Address": form_data.get('6', ""),
                "City": form_data.get('7', ""),
                "Taluk": form_data.get('8', ""),
                "Disrict": form_data.get('9', ""),
                "State": form_data.get('10', ""),
                "Pincode": form_data.get('11', ""),
                "pass": form_data.get('12', ""),
                "completed": ""
            }
            
            companies_form_api = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
            request_body = {
                    "Action": "Add",
                    "Properties": {
                        "Locale": "en-IN"
                    },
                    "Rows":[form_entry]
                }
            headers = {"Content-Type":"application/json"}
            # companies_response = requests.post(companies_form_api, json=request_body, headers=headers)
        
            return render_template("auditor/shareLink.html", form_entry=form_entry, link="/login")
            # if companies_response.status_code == 200:
            #     return render_template("auditor/shareLink.html", form_entry=form_entry, link="/login")
            # else:
            #     return redirect(url_for('auditor_dash.dash_page'))
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auditor_auth.login_page'))
