from flask import Blueprint, request, render_template, redirect, url_for, session
from ..generateFormView import generate_html_form
from .generateCompaniesView import geenerate_companies_view
import requests

auditor_dash = Blueprint('auditor_dash', __name__)

@auditor_dash.route('/auditor/dash')
def dash_page():
    if 'auditor_logged_in' in session:
        if 'company' in request.args and 'type' in request.args and 'name' in request.args:
            # --------------------------------------------------------
            # Get company name and type from session data
            company = request.args.get('name')
            company_type = request.args.get('type')  # Assuming 'company_type' is also stored in the session
            company_id = request.args.get('company')
            water_matrix_html = f'<a href="matrix?type={company_type}&company={company_id}&name={company}"><button>Link to Water Matrix</button></a> </br></br>'
            form_view = "Cannot access the forms"
            
            form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            
            request_body = {
                    "Action": "Find",
                    "Properties": {
                        "Locale": "en-IN"
                    },
                    "Rows":[]
                }
            headers = {"Content-Type":"application/json"}
            form_response = requests.post(form_api_url, json=request_body, headers=headers)

            if form_response.status_code == 200:
                form_view = generate_html_form(form_response.json(), company_type=company_type, id=company_id)
                        
            # Render the dashboard template with the company name and type
            return render_template('formPage.html', company=company, form_html = water_matrix_html+form_view)
        
            # --------------------------------------------------------
        else:
            # Get company name and type from session data
            form_view = "Cannot access the forms"
            companies_html = "Cannot access Companies"

            form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            companies_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            
            request_body = {
                    "Action": "Find",
                    "Properties": {
                        "Locale": "en-IN"
                    },
                    "Rows":[]
                }
            headers = {"Content-Type":"application/json"}
            # form_response = requests.post(form_api_url, json=request_body, headers=headers)
            companies_response = requests.post(companies_api_url, json=request_body, headers=headers)
            
            if companies_response.status_code == 200:
                companies_html = geenerate_companies_view(companies_response.json())
            
            # Render the dashboard template with the company name and type
            return render_template('auditor/dash.html', blocks_html=companies_html)
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auditor_auth.login_page'))
