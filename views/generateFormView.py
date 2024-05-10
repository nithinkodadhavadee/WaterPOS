from .generateTableView import generate_table_view
from flask import Blueprint, render_template, redirect, url_for, session
import requests

def generate_html_form(form_data, company_type=None, id=None):
    count = 0
    filtered_response = []
    if company_type == None:
        company_type=session.get('type')
    if id == None:
        id = session.get("ID")


    print(id)
    print(company_type)

    try:
        ref_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/" 
        ref_api_queries = " Multi Input Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
            
        request_body = {
            "Action": "Find",
                "Properties": {
                    "Locale": "en-IN"
                },
                "Rows":[]
            }
        headers = {"Content-Type":"application/json"}
        response = requests.post(ref_api_url+ company_type +ref_api_queries, json=request_body, headers=headers)
        json_response = response.json()
        print(json_response)
        for field in json_response: 
            if field["Project ID"] == id:
                filtered_response.append(field)

        print(filtered_response)
    except:
        pass
    html_code = ""
    for field in form_data:
        if field["Type"] == "label":
            # If it's a label, add a heading
            html_code += f'<h3>{field["Text"]}</h3>'
        else:
            count = count+1

            # Otherwise, create the input element based on the field type
            html_code += f'<label>{count}. {field["Text"]}:</label>'
            
            # Add description if available
            if field["Description"]:
                html_code += f'<p>{field["Description"]}</p>'
            # Add required attribute if necessary
            if field["Required"] == "yes":
                html_code += f'<span style="color:red;">*</span>'

            if field["Type"] == "text":
                html_code += f'<input type="text" name="{field["_RowNumber"]}">'
            elif field["Type"] == "date":
                html_code += f'<input type="date" placeholder="dd-mm-yyyy" name="{field["_RowNumber"]}">'
            elif field["Type"] == "number":
                html_code += f'<input type="number" name="{field["_RowNumber"]}">'
            elif field["Type"] == "email":
                html_code += f'<input type="email" name="{field["_RowNumber"]}">'
            elif field["Type"] == "list":
                if response.status_code == 200:
                    try:
                        ref_form = filtered_response
                        html_code += generate_table_view(ref_form, field["Text"])
                    except:
                        pass
                else:
                    html_code += '<div>Cannot generate the form</div>'
            elif field["Type"] == "longtext":
                html_code += f'<textarea name="{field["_RowNumber"]}" rows="4" cols="50"></textarea>'
            elif field["Type"] == "float":
                html_code += f'<input type="number" step="0.01" name="{field["_RowNumber"]}">'
            elif field["Type"] == "url":
                html_code += f'<input type="url" name="{field["_RowNumber"]}">'

            html_code += '<br><br>'

    return html_code