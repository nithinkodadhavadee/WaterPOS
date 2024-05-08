from flask import Flask, request, render_template
import requests

app = Flask(__name__, template_folder='./app/templates')


# Function to generate Sl No
def generate_sl_no(group, index):
    return f"{group}{index + 1}"


@app.route('/', methods=['GET'])
def getData():
    # Get the query parameters
    company = request.args.get('company')
    companyType = request.args.get('type')

    # Perform some logic based on the parameters
    if company is None or companyType is None:
        return render_template('error.html', message='Both company and type parameters are required.'), 400

    # Placeholder for data retrieval logic based on company and type
    # You can replace this with your actual data retrieval code
    data = {
        'company': company,
        'type': companyType,
        'info': 'Placeholder data for company {} of type {}'.format(company, companyType)
    }

    appsheetApi = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/" + companyType + "/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"
    
    # Request body data
    requestBodyData = {
        "Action": "Find",
        "Properties": {
            "Locale": "en-IN"
        },
        "Rows": []
    }
    
    # Make a POST request to the external API
    response = requests.post(appsheetApi, json=requestBodyData)
    print(response)
    try:
        json_data = response.json()
    except:
        return render_template('error.html', message='No data available for the specified company.'), 404

    # Extracting data for the specified company
    company_data = {}
    for row in json_data:
        if row.get('Company') == company:
            company_data = row
            break
    
    if not company_data:
        return render_template('error.html', message='No data available for the specified company.'), 404
    
    # Dictionary to map each attribute to its group
    attribute_groups = {
        "Quantity of Raw water drawn (Bulk water supplied) from BWSSB main (in KLD)": "Group A",
        "Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD)": "Group A",
        "Quantity of Bottled water supplied from the vendor for potable/ drinking purpose (in KLD)": "Group A",
        "Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)": "Group A",
        "Freshwater supplied to Industrial processes": "Group B",
        "Freshwater supplied to canteen": "Group B",
        "Freshwater supplied to RO": "Group B",
        "Freshwater supplied for domestic use(it includes building wise restroom and other uses)": "Group B",
        "Freshwater supplied to cooling towers (no values should overlap)": "Group B",
        "Freshwater supplied for any other usage (like floor cleaning, gardening, vehicle washing, construction purpose etc.)": "Group B",
        "Volume of Waste water generated from all places like Canteen, restrooms building wise, industrial processes, Ro reject, Water treatment plant, etc (in KLD)": "Group C",
        "Quantity of Treated Waste water utilized in KLD Gardening/ Lawn": "Group D",
        "Quantity of Treated Waste water utilized in KLD;  Toilet Flush:": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Cooling purpose:": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Rough wash purpose:": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Floor cleaning:": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Construction purpose": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Green Belt development": "Group D",
        "Quantity of Treated Waste water utilized in KLD; Any other Usage:": "Group D",
        "Treated waste water discharge to outside the campus boundries": "Group E"
    }

    # Extracting relevant data attributes for the table along with their groups
    table_data = {}
    for key, value in company_data.items():
        if key in attribute_groups:
            group = attribute_groups[key]
            if value and value != "0" and value != "null":
                if group not in table_data:
                    table_data[group] = {}
                table_data[group][key] = value
    
    return render_template('index.html', company=company, table_data=table_data)


@app.route('/data', methods=['GET'])
def generateViews():
    # Get the query parameters
    company = request.args.get('company')
    companyType = request.args.get('type')

    # Perform some logic based on the parameters
    if company is None or companyType is None:
        return render_template('error.html', message='Both company and type parameters are required.'), 400

    # Placeholder for data retrieval logic based on company and type
    # You can replace this with your actual data retrieval code
    data = {
        'company': company,
        'type': companyType,
        'info': 'Placeholder data for company {} of type {}'.format(company, companyType)
    }

    appsheetApi = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/A0/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"
    appsheetFreshWaterApi = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/A1/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"
    appsheetStpApi = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/A2/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"
    appsheetEtpApi = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/A3/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"

    # Request body data
    requestBodyData = {
        "Action": "Find",
        "Properties": {
            "Locale": "en-IN"
        },
        "Rows": []
    }
    
    response = requests.post(appsheetApi, json=requestBodyData)
    formEntries = response.json()
    response = requests.post(appsheetFreshWaterApi, json=requestBodyData)
    freshWaterEntries = response.json()
    response = requests.post(appsheetStpApi, json=requestBodyData)
    stpEntries = response.json()
    response = requests.post(appsheetEtpApi, json=requestBodyData)
    etpEntries = response.json()

    filteredData = {
        "form": {},
        "freshWater": [],
        "stp": [],
        "etp": []
    }
    for x in formEntries:
        if x["ID"] == company:
            filteredData["form"] = x
    for x in freshWaterEntries:
        if x["Project ID"] == company:
            filteredData["freshWater"].append(x)
    for x in stpEntries:
        if x["Project ID"] == company:
            filteredData["stp"].append(x)
    for x in etpEntries:
        if x["Project ID"] == company:
            filteredData["etp"].append(x)
    
    print(filteredData)
    
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
            "Quantity of Treated Waste water utilized in KLD - Green Belt development (excluding the lawn and garden area)"
        ],
        "E" : [
            "Qty of treated wastewater coming out of ETP",
            "Treated waste water discharge to outside the campus boundries"
        ]
    }

    groupData = {
        "A": [
            "Total base area of the plot/ dimension of the campus (in Sq. M. or Sq. Ft. or Acres) - Area",
            "Quantity of Raw water drawn (Bulk water supplied) from BWSSB main (in KLD) - Quantity",
            
        ],
        "B": [],
        "C": [],
        "D": [],
        "E": []
    }
    table_data = []

    for group, keys in individualData.items():
        total_volume = 0
        for index, key in enumerate(keys):
            value = filteredData['form'].get(key, "")  
            if value != 0 and value != "":
                table_data.append([generate_sl_no(group, index), key, value, ""])
                # Calculate total volume for each group
                if value:
                    try:
                        total_volume += float(value)
                    except ValueError:
                        pass  # Ignore if the value is not a valid float
        # Add a row for the total volume of the group
        table_data.append(["Total", f"Total {group}", str(total_volume), ""])

    return render_template('watermatrix.html', table_data=table_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
