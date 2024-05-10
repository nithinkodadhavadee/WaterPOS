from flask import Blueprint, request, render_template
import requests

auditor_matrix = Blueprint('auditor_matrix', __name__)

# Function to generate Sl No
def generate_sl_no(group, index):
    return f"{group}{index + 1}"


@auditor_matrix.route('/auditor/matrix', methods=['GET'])
def generateViews():
    # Get the query parameters
    company = request.args.get('company')
    company_type = request.args.get('type')
    company_name = request.args.get('name')

    if company is None or company_type is None:
        return render_template('error.html', message='Both company and type parameters are required.'), 400

    form_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
    multi_input_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Automobile Multi Input Form/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
        
    # Request body data
    requestBodyData = {
        "Action": "Find",
        "Properties": {
            "Locale": "en-IN"
        },
        "Rows": []
    }
    
    response = requests.post(form_api_url, json=requestBodyData)
    form_entries = response.json()
    response = requests.post(multi_input_api_url, json=requestBodyData)
    multi_input_entries = response.json()


    filteredData = {
        "form": {},
        "multi": []
    }
    print(form_entries)
    for x in form_entries:
        print(x)
        if x["ID"] == company:
            filteredData["form"] = x
    for x in multi_input_entries:
        if x["Project ID"] == company:
            filteredData["multi"].append(x)
            
    
    individualData = {
        "A" : [
            "Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)",
            "Quantity of Bottled water supplied from the vendor for potable/ drinking purpose (in KLD)"
        ],
        "B" : [
            "Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)",
            "Freshwater supplied to RO"
        ],
        "C" : [],
        "D" : [
            "Quantity of Treated Waste water utilized in KLD - Construction purpose",
            "Quantity of Treated Waste water utilized in KLD - Gardening/ Lawn",
            "Quantity of Treated Waste water utilized in KLD - Green Belt development (excluding the lawn and garden area)",
            "Volume of treated wastewater coming out of STP in KLD"
        ],
        "E" : [
            "Qty of treated wastewater coming out of ETP",
            "What is the treated wastewater discharged outside the campus boundary"
        ]
    }

    groupData = {
        "A": [
            "Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Area",
            "Quantity of Raw water drawn (Bulk water supplied) from BWSSB main (in KLD) - Quantity",
            "Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD) - Quantity"
            
        ],
        "B": [
            "Actual Quantity of Fresh/ Raw water stored/ collected in the sumps in KLD - actual quantity",
            "TotalQuantity of Fresh/ Raw water Supplied in KLD - Quantity",
            "Freshwater supplied for domestic use(it includes building wise restroom and other uses) - Quantity",
            "Freshwater supplied to canteen - Quantity",
            "Freshwater supplied to Industrial processes (combined or in parts, if avialable) - Quantity",
            "Freshwater supplied to softners / cooling towers (no values should overlap) - Quantity",
            "Freshwater supplied for any other usage (like floor cleaning, gardening, vehicle washing, construction purpose etc.)...not included till now - Quantity",
        ],
        "C": [
            "Volume of Waste water generated from all places like Canteen, restrooms building wise, Ro reject, Water treatment plant, etc (in KLD) reaching the STP - Quantity"
        ],
        "D": [],
        "E": [
            "Volume of Effluent generated (in KLD) - Quantity",
            "Quantity of Treated Effluent Utilized (in KLD) - Quantity",
            "Quantity of Treated Effluent utilized in KLD - Quantity"
        ]
    }
    
    table_data = {
        "A" : {},
        "B" : {},
        "C" : {},
        "D" : {},
        "E" : {}
    }

    for key in filteredData["form"]:
        if key in individualData['A']:
            table_data["A"][key] = float(filteredData["form"][key])
        if key in individualData['B']:
            table_data["B"][key] = float(filteredData["form"][key])
        if key in individualData['C']:
            table_data["C"][key] = float(filteredData["form"][key])
        if key in individualData['D']:
            table_data["D"][key] = float(filteredData["form"][key])
        if key in individualData['E']:
            if key == "What is the treated wastewater discharged outside the campus boundary":
                table_data["E"]["Treated Wastewater Discharge to outside the campus boundary"] = float(filteredData["form"][key])
            else:
                table_data["E"][key] = float(filteredData["form"][key])



    for item in filteredData["multi"]:
        for key in item:
            if key in groupData['A']:
                try:
                    table_data["A"][key] = table_data["A"].get(key, 0) + float(item[key])
                except KeyError:
                    table_data["A"][key] = float(filteredData["form"][key])
                except ValueError:
                    pass
            if key in groupData['B']:
                try:
                    table_data["B"][key] = table_data["B"].get(key, 0) + float(item[key])
                except KeyError:
                    table_data["B"][key] = float(filteredData["form"][key])
                except ValueError:
                    pass
            if key in groupData['C']:
                try:
                    table_data["C"][key] = table_data["C"].get(key, 0) + float(item[key])
                except KeyError:
                    table_data["C"][key] = float(filteredData["form"][key])
                except ValueError:
                    pass
            if key in groupData['D']:
                try:
                    table_data["D"][key] = table_data["D"].get(key, 0) + float(item[key])
                except KeyError:
                    table_data["D"][key] = float(filteredData["form"][key])
                except ValueError:
                    pass
            if key in groupData['E']:
                try:
                    table_data["E"][key] = table_data["E"].get(key, 0) + float(item[key])
                except KeyError:
                    table_data["E"][key] = float(filteredData["form"][key])
                except ValueError:
                    pass

    # Process the table data for rendering in the HTML template
    processed_table_data = []

    totals = [0, 0, 0, 0, 0]
    # Iterate over each group
    for group, particulars in table_data.items():
        # Iterate over each key-value pair within the group
        keyTotal = 0
        for key, volume in particulars.items():
            # Generate Sl No
            sl_no = generate_sl_no(group, list(particulars.keys()).index(key))
            keyTotal = keyTotal+volume
            # Append the row to the processed_table_data
            processed_table_data.append([sl_no, key, volume, ""])  # Volume (%) is empty for now

        if(group == "A"):
            totals[0] = keyTotal
            processed_table_data.append(["", "Total Raw Water Supply A", keyTotal, ""])
            processed_table_data.append(["", "", "", ""])
        elif(group == "B"):
            totals[1] = keyTotal
            processed_table_data.append(["", "Total Raw Water Usage B", keyTotal, ""])
            processed_table_data.append(["", "", "", ""])
        elif(group == "C"):
            totals[2] = keyTotal
            processed_table_data.append(["", "", "", ""])
        elif(group == "D"):
            totals[3] = keyTotal
            processed_table_data.append(["", "Total Recycled Water distribution D", keyTotal, ""])
            processed_table_data.append(["", "", "", ""])
        elif(group == "E"):
            totals[4] = keyTotal
            processed_table_data.append(["", "", "", ""])

    processed_table_data.append(["", "The difference between Source(A) and Consumption (B)", totals[0]-totals[1], ""])
    # Pass the processed_table_data to the HTML template for rendering
    return render_template('auditor/watermatrix.html', table_data=processed_table_data, company_name = company_name, company_id = company)
