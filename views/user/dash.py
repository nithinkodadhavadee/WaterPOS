from flask import Blueprint, render_template, redirect, url_for, session
from ..generateFormView import generate_html_form
from ..generateBlocksView import generate_blocks_view
import requests

dash = Blueprint('dash', __name__)

@dash.route('/dash')
def dash_page():
    if 'logged_in' in session and session.get('logged_in') == True:
        # Get company name and type from session data
        company = session.get('company')
        company_type = session.get('type')  # Assuming 'company_type' is also stored in the session
        company_id = session.get('ID')

        form_view = "Cannot access the forms"
            
        # form_api_url = f"https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/{company_type} Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        form_api_url = f"https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
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

        # response = requests.post(ref_api_url+ company_type +ref_api_queries, json=request_body, headers=headers)
        response = requests.post(ref_api_url+ "Automobile" +ref_api_queries, json=request_body, headers=headers)

        print(response.status_code)
        print(response.text)
        json_response = response.json()

        response = requests.post(ref_api_url+ "Automobile" +entries_api_queries, json=request_body, headers=headers)
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

        return render_template('categoryFormPage.html', company=company, form_html = form_html, company_type=company_type, blocks_html=blocks_html)
        
        # form_view = "Cannot access the forms"
        # blocks_html = "Cannot access buildings"

        # form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Questions/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        # blocks_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Blocks Entries/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
        # request_body = {
        #         "Action": "Find",
        #         "Properties": {
        #             "Locale": "en-IN"
        #         },
        #         "Rows":[]
        #     }
        # headers = {"Content-Type":"application/json"}
        # form_response = requests.post(form_api_url, json=request_body, headers=headers)
        # blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

        # form_html = []
        # form_categories = [[]]
        # if form_response.status_code == 200:
        #     # form_view = generate_html_form(form_response.json())
        #     form_question = form_response.json()
        #     for x in form_question:
        #         if x["Type"] == "label":
        #             form_categories.append([])
        #         form_categories[-1].append(x)
        # if blocks_response.status_code == 200:
        #     blocks_html = generate_blocks_view(blocks_response.json(), company_id)

        # for x in form_categories:
        #         try:
        #             form_generated = generate_html_form(x, company_type=company_type, id=company_id)
                    
        #             form_html.append(form_generated)
        #         except:
        #             form_html.append("Cannot generate Form") 
        # return render_template('categoryformPage.html', company=company, form_html = form_html, blocks_html=blocks_html, company_type=company_type) 
            
        # # Render the dashboard template with the company name and type
        # # return render_template('user/dash.html', company=company, company_type=company_type, blocks_html=blocks_html, form_html = form_view)
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auth.login_page'))
