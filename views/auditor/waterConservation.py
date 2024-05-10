from flask import Blueprint, render_template, redirect, url_for, session, request
import requests

conservation = Blueprint('conservation', __name__)

@conservation.route('/auditor/conservation')
def conservation_view():
    if 'auditor_logged_in' in session:
        company = request.args.get('company')
        company_type = request.args.get('type')
        company_name = request.args.get('name')
        
        form_view = "Cannot access the forms"
        blocks_html = "Cannot access buildings"

        form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        multi_form_api = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Multi Input Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        blocks_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Blocks Entries/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
        request_body = {
                "Action": "Find",
                "Properties": {
                    "Locale": "en-IN"
                },
                "Rows":[]
            }
        headers = {"Content-Type":"application/json"}
        # form_response = requests.post(form_api_url, json=request_body, headers=headers)
        multi_form_response = requests.post(multi_form_api, json=request_body, headers=headers)
        blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

        table_data = {
            "existingBuildings": [],
            "existingArea" : [],
            "existingTotal": 0,
            "proposedBuilding": [],
            "proposedArea" : [],
            "proposedTotal" : 0
        }
        if multi_form_response.status_code == 200 and blocks_response.status_code == 200:
            multi_json = multi_form_response.json()
            blocks_json = blocks_response.json()
            for x in multi_json:
                try: 
                    if x["Project ID"] == company and x["Name of the buildings from where the rain water is collected - Building"] != '':    
                        table_data["existingBuildings"].append(x["Name of the buildings from where the rain water is collected - Building"])
                        table_data["existingArea"].append(float(x["Name of the buildings from where the rain water is collected - Area"]))
                except:
                    pass
            
            building_area = 0
            for x in blocks_json:
                try:
                    building_area = building_area+float(x["Roof Area"])
                    if x["Company ID"] == company:
                        if x["Name"] not in table_data["existingBuildings"]:
                            table_data["proposedBuilding"].append(x["Name"])
                            table_data["proposedArea"].append(float(x["Roof Area"]))
                except:
                    pass
                
            table_data["existingTotal"] = len(table_data["existingBuildings"])
            table_data["proposedTotal"] = len(table_data["proposedBuilding"])

            open_areas = [0,0,building_area,0,0]
            for x in multi_json:
                try: 
                    if x["Project ID"] == company:
                        if(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Names"]) == "Total Area of the plot":
                            open_areas[0] = float(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Area"])
                        if(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Names"]) == "Garden/Lawn Area (maintained)":
                            open_areas[1] = float(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Area"])
                        if(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Names"]) == "Green Belt area (excluding garden or lawn area)":
                            open_areas[3] = float(x["Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Area"])
                except:
                    pass

            open_areas[4] = open_areas[0] - open_areas[1] - open_areas[2] - open_areas[3] 
            total_open_area = open_areas[4] 
            open_spaces = []
            open_spaces.append(open_areas)
            open_spaces.append(["Open Spaces including pavments, approach roads & landscapes", total_open_area, 0,35, 0.890, total_open_area*0.35*0.89, total_open_area*0.35*0.89/365])
            
        # Render the dashboard template with the company name and type
        return render_template('auditor/conservation.html', company=company_name, company_type=company_type, table_data=table_data, open_spaces=open_spaces)
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auditor_auth.login_page'))


# from flask import Blueprint, render_template, redirect, url_for, session, request
# import requests

# conservation = Blueprint('conservation', __name__)

# @conservation.route('/auditor/conservation')
# def conservation_view():
#     if 'logged_in' in session:
#         company = request.args.get('company')
#         company_type = request.args.get('type')
#         company_name = request.args.get('name')
        
#         form_view = "Cannot access the forms"
#         blocks_html = "Cannot access buildings"

#         form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
#         multi_form_api = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Multi Input Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
#         blocks_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Blocks Entries/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
#         request_body = {
#                 "Action": "Find",
#                 "Properties": {
#                     "Locale": "en-IN"
#                 },
#                 "Rows":[]
#             }
#         headers = {"Content-Type":"application/json"}
#         # form_response = requests.post(form_api_url, json=request_body, headers=headers)
#         multi_form_response = requests.post(multi_form_api, json=request_body, headers=headers)
#         blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

#         table_data = {
#             "existingBuildings": [],
#             "existingArea" : [],
#             "existingTotal": 0,
#             "proposedBuilding": [],
#             "proposedArea" : [],
#             "proposedTotal" : 0
#         }
#         if multi_form_response.status_code == 200 and blocks_response.status_code == 200:
#             multi_json = multi_form_response.json()
#             blocks_json = blocks_response.json()
#             for x in multi_json:
#                 try: 
#                     if x["Project ID"] == company and x["Name of the buildings from where the rain water is collected - Building"] != '':    
#                         table_data["existingBuildings"].append(x["Name of the buildings from where the rain water is collected - Building"],)
#                         table_data["existingArea"].append(x["Name of the buildings from where the rain water is collected - Area"])
#                 except:
#                     pass
            
#             for x in blocks_json:
#                 try:
#                     if x["Company ID"] == company:
#                         if x["Name"] not in table_data["existingBuildings"]:
#                             table_data["proposedBuilding"].append(x["Name"])
#                             table_data["proposedArea"].append(x["Roof Area"])
#                 except:
#                     pass
                
#             print(table_data)

        
        
#         # Render the dashboard template with the company name and type
#         return render_template('auditor/conservation.html', company=company_name, company_type=company_type, table_data = table_data)
#     else:
#         # Redirect to the login page if user is not authenticated
#         return redirect(url_for('auditor_auth.login_page'))
