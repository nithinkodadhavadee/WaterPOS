from flask import Blueprint, render_template, redirect, url_for, session
from ..generateFormView import generate_html_form
from .generateBlocksView import generate_blocks_view
import requests

dash = Blueprint('dash', __name__)

@dash.route('/dash')
def dash_page():
    if 'logged_in' in session:
        # Get company name and type from session data
        company = session.get('company')
        company_type = session.get('type')  # Assuming 'company_type' is also stored in the session
        company_id = session.get('ID')
        form_view = "Cannot access the forms"
        blocks_html = "Cannot access buildings"

        form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        blocks_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Blocks Entries/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
        request_body = {
                "Action": "Find",
                "Properties": {
                    "Locale": "en-IN"
                },
                "Rows":[]
            }
        headers = {"Content-Type":"application/json"}
        form_response = requests.post(form_api_url, json=request_body, headers=headers)
        blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

        print(form_response.status_code, blocks_response.status_code)
        if form_response.status_code == 200:
            form_view = generate_html_form(form_response.json())
        if blocks_response.status_code == 200:
            blocks_html = generate_blocks_view(blocks_response.json(), company_id)

        
        # Render the dashboard template with the company name and type
        return render_template('user/dash.html', company=company, company_type=company_type, blocks_html=blocks_html, form_html = form_view)
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auth.login_page'))
