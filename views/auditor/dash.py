from flask import Blueprint, request, render_template, redirect, url_for, session
from ..generateFormView import generate_html_form
from .generateCompaniesView import geenerate_companies_view
from ..generateBlocksView import generate_blocks_view

import requests

auditor_dash = Blueprint('auditor_dash', __name__)

@auditor_dash.route('/auditor/dash')
def dash_page():
    if 'auditor_logged_in' in session and session['auditor_logged_in'] == True:
        if 'company' in request.args and 'type' in request.args and 'name' in request.args:
            # --------------------------------------------------------
            # Get company name and type from session data
            company = request.args.get('name')
            company_type = request.args.get('type')  # Assuming 'company_type' is also stored in the session
            company_id = request.args.get('company')
            water_matrix_html = f'<a href="matrix?type={company_type}&company={company_id}&name={company}"><button>Link to Water Matrix</button></a> </br></br>'
            form_view = "Cannot access the forms"
            
            form_api_url = f"https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/{company_type} Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            
            request_body = {
                    "Action": "Find",
                    "Properties": {
                        "Locale": "en-IN"
                    },
                    "Rows":[]
                }
            headers = {"Content-Type":"application/json"}
            form_response = requests.post(form_api_url, json=request_body, headers=headers)

            # if form_response.status_code == 200:
            #     form_view = generate_html_form(form_response.json(), company_type=company_type, id=company_id)
                        
            # # Render the dashboard template with the company name and type
            # return render_template('formPage.html', company=company, form_html = water_matrix_html+form_view)
        
            form_html = []
            form_categories = [[]]
            if form_response.status_code == 200:
                form_question = form_response.json()
                for x in form_question:
                    if x["Type"] == "label":
                        form_categories.append([])
                    form_categories[-1].append(x)
              

            ref_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/" 
            ref_api_queries = " Multi Input Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            entries_api_queries = " Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            filtered_response = []
            filtered_entries = []

            response = requests.post(ref_api_url+ company_type +ref_api_queries, json=request_body, headers=headers)
            json_response = response.json()

            response = requests.post(ref_api_url+ company_type +entries_api_queries, json=request_body, headers=headers)
            entries_response = response.json()

            for field in json_response: 
                if field["Project ID"] == company_id:
                    filtered_response.append(field)

            for row in entries_response:
                if row["ID"] == company_id:
                    filtered_entries = row
        

            blocks_html = "Cannot access buildings"
            blocks_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Blocks Entries/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

            if blocks_response.status_code == 200:
                blocks_html = generate_blocks_view(blocks_response.json(), company_id)
        
            all_blocks = blocks_response.json()
            blocks = []
            for block in all_blocks:
                if block['Company ID'] == company_id:
                    blocks.append(block)


            for x in form_categories:
                try:
                    form_generated = generate_html_form(x, company_type=company_type, id=company_id, filtered_response=filtered_response, filtered_entries=filtered_entries, blocks=blocks)
                    # print(x)
                    form_html.append(form_generated)
                except:
                    form_html.append("Cannot generate Form") 

            misc_button = '<button class="tablinks" style="background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s;" onclick="openTab(event, \'misce\')">Miscellaneous Questions</button>'
            return render_template('categoryFormPage.html', company=company, water_matrix=water_matrix_html, form_html = form_html, company_type=company_type, blocks_html=blocks_html, misc_button=misc_button)
            
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
