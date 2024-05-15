from .generateTableView import generate_table_view
from flask import Blueprint, render_template, redirect, url_for, session
import requests

def generate_html_form(form_data, company_type=None, id=None, submit_link=None, filtered_response = [], filtered_entries = []):
    
    count = 0
    if company_type == None:
        company_type=session.get('type')
    if id == None:
        id = session.get("ID")


    html_code = ""
    if submit_link:
        html_code += f'<form action="{submit_link}" method="post">'
    else:
        html_code += '<form>'
    for field in form_data:
        if field["Type"] == "label":
            # If it's a label, add a heading
            html_code += f'<h3>{field["Text"]}</h3>'
        else:
            count = count+1

            # Otherwise, create the input element based on the field type
            html_code += f'<label>{count}. {field["Text"]}:</label>'
            
            # Add description if available
            # if field["Description"]:
            #     html_code += f'<p>{field["Description"]}</p>'
            # Add required attribute if necessary
            if field["Required"] == "yes":
                html_code += f'<span style="color:red;">*</span>'

            try:
                if field["Type"] == "text":
                    html_code += f'<input type="text" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "date":
                    html_code += f'<input type="date" placeholder="dd-mm-yyyy" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "number":
                    html_code += f'<input type="number" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "email":
                    html_code += f'<input type="email" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "list":
                    try:
                        ref_form = filtered_response
                        html_code += generate_table_view(ref_form, field["Text"])
                    except:
                        pass
                elif field["Type"] == "longtext":
                    html_code += f'<textarea name="{field["_RowNumber"]}" rows="4" cols="50" value="{filtered_entries[field["Text"]]}"></textarea>'
                elif field["Type"] == "float":
                    html_code += f'<input type="number" step="0.01" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "url":
                    html_code += f'<input type="url" name="{field["_RowNumber"]}" value="{filtered_entries[field["Text"]]}">'
                elif field["Type"] == "bool":
                    html_code += f'<input type="checkbox" {'checked' if filtered_entries[field["Text"]] == '1' else ''}>'
                elif field["Type"] == "select":
                    values = field["Description"].split(',')
                    select_html = f'<select name="{field["_RowNumber"]}">'
                    for value in values:
                        selected = 'selected' if filtered_entries[field["Text"]] == value else ''
                        select_html += f'<option value={value} {selected}>{value}</option>'
                    html_code += f'{select_html}</select>'

            except:
                if field["Type"] == "text":
                    html_code += f'<input type="text" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "date":
                    html_code += f'<input type="date" placeholder="dd-mm-yyyy" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "number":
                    
                    html_code += f'<input type="number" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "email":
                    html_code += f'<input type="email" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "list":
                    try:
                        ref_form = filtered_response
                        html_code += generate_table_view(ref_form, field["Text"])
                    except:
                        pass
                elif field["Type"] == "longtext":
                    html_code += f'<textarea name="{field["_RowNumber"]}" rows="4" cols="50" ></textarea>'
                elif field["Type"] == "float":
                    html_code += f'<input type="number" step="0.01" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "url":
                    html_code += f'<input type="url" name="{field["_RowNumber"]}" >'
                elif field["Type"] == "bool":
                    html_code += f'<input type="checkbox" disabled>'
                elif field["Type"] == "select":
                    values = field["Description"].split(',')
                    select_html = f'<select name="{field["_RowNumber"]}">'
                    for value in values:
                        select_html += f'<option value={value}>{value}</option>'
                    html_code += f'{select_html}</select>'

            html_code += '<br><br>'
    html_code += '<button type="submit">Submit</button></form>'
    return html_code
