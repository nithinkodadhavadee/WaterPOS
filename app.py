from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder='./app/templates')

@app.route('/', methods=['GET'])
def post_request():
    EXTERNAL_API_URL = "https://www.appsheet.com/api/v2/apps/1d97fa54-f86b-48cf-a81f-cc5edb15b62d/tables/" + "Automobile" + "/Action?applicationAccessKey=V2-FMmuN-5Ldnj-qzcie-6AmdR-wtMP7-bt8Mw-HdTgA-4GR3y"
    
    # Request body data
    request_body_data = {
        "Action": "Find",
        "Properties": {
            "Locale": "en-IN"
        },
        "Rows": []
    }
    
    # Make a POST request to the external API
    response = requests.post(EXTERNAL_API_URL, json=request_body_data)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get response data from the external API
        api_response_data = response.json()
        
        # Initialize dictionaries to store data for each group
        group_data = {
            'Group A': {},
            'Group B': {},
            'Group C': {},
            'Group D': {},
            'Group E': {}
        }
        
        # Define the keys you want to extract for each group
        keys_to_extract = {
            'Group A': [
                'Quantity of Raw water drawn (Bulk water supplied) from BWSSB main (in KLD)',
                'Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD)',
                'Quantity of Bottled water supplied from the vendor for potable/ drinking purpose (in KLD)',
                'Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)'
            ],
            'Group B': [
                'Freshwater supplied to Industrial processes (combined or in parts, if avialable',
                'Freshwater supplied to canteen',
                'Freshwater supplied to RO',
                'Freshwater supplied for domestic use(it includes building wise restroom and other uses)',
                'Freshwater supplied to cooling towers (no values should overlap)',
                'Freshwater supplied for any other usage (like floor cleaning, gardening, vehicle washing, construction purpose etc.)'
            ],
            'Group C': [
                'Volume of Waste water generated from all places like Canteen, restrooms building wise, industrial processes, Ro reject, Water treatment plant, etc (in KLD)'
            ],
            'Group D': [
                'Quantity of Treated Waste water utilized in KLD Gardening/ Lawn',
                'Quantity of Treated Waste water utilized in KLD; Toilet Flush:',
                'Quantity of Treated Waste water utilized in KLD; Cooling purpose:',
                'Quantity of Treated Waste water utilized in KLD; Rough wash purpose:',
                'Quantity of Treated Waste water utilized in KLD; Floor cleaning:',
                'Quantity of Treated Waste water utilized in KLD; Construction purpose',
                'Quantity of Treated Waste water utilized in KLD; Green Belt development',
                'Quantity of Treated Waste water utilized in KLD; Any other Usage:'
            ],
            'Group E': [
                'Treated waste water discharge to outside the campus boundries'
            ]
        }
        
        # Iterate over each item in the API response
        for row in api_response_data:
            # Iterate over each group
            for group, keys in keys_to_extract.items():
                # Initialize dictionary for the group if not present
                if group not in group_data:
                    group_data[group] = {}
                # Extract keys for the current group
                for key in keys:
                    if key in row:
                        # Add key-value pair to the corresponding group dictionary
                        group_data[group][key] = row[key]
        
        # Render the response HTML template with the data
        print(api_response_data)
        return render_template('index.html', group_data=group_data)
    else:
        print("Error: Failed to fetch data from external API")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)