from flask import Blueprint, render_template, redirect, url_for, session, request
import requests

report = Blueprint('report', __name__)

@report.route('/auditor/report')
def report_view():
    if 'auditor_logged_in' in session:
        company = request.args.get('company')
        company_type = request.args.get('type')
        company_name = request.args.get('name')
        
        # form_view = "Cannot access the forms"
        # blocks_html = "Cannot access buildings"

        company_api_url = "https://www.appsheet.com/api/v2/apps/80ca4d2d-67ba-4f5e-9dc2-6c954355c70c/tables/Projects/Action?applicationAccessKey=V2-qCjEs-Vnmn2-4X5Zm-bDW8b-LUC3U-k3i1H-9DovC-fkSY6"
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
        
        company_request_body = {
            "Action": "Find",
            "Properties": {
                "Locale": "en-IN"
                },
                "Rows":[
                {
                    "Name": company_name
                }
            ]
        }
        headers = {"Content-Type":"application/json"}

        company_response = requests.post(company_api_url, json=company_request_body, headers=headers)
        company_response = company_response.json()
        
        form_response = requests.post(form_api_url, json=request_body, headers=headers)
        form_response = form_response.json()
        filtered_form_response = []
        for x in form_response:
            if x["ID"] == company:
                filtered_form_response = x

        filtered_multi_form_response = []
        multi_form_response = requests.post(multi_form_api, json=request_body, headers=headers)
        multi_form_response = multi_form_response.json()
        for x in multi_form_response:
            if x["Project ID"] == company:
                filtered_multi_form_response.append(x)

        total_multi_form_response = {}
        for x in filtered_multi_form_response:
            for key in x:
                try:
                    total_multi_form_response[key] = total_multi_form_response.get(key, 0) + float(x[key])
                except ValueError:
                    pass
        # blocks_response = requests.post(blocks_api_url, json=request_body, headers=headers)

        borewellString = ""
        tankerString = ""
        if filtered_form_response["Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)"]:
            tankerString = f"procures {filtered_form_response['Quantity of Raw water supplied from the Tankers/ Vendor for domestic/ non domestic purpose (in KLD)']}KL of water per day from a tanker, storing the raw water in designated sumps before consumption for various purposes."
        
        if total_multi_form_response.get("Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD) - Quantity",0):
            if tankerString == "":
                borewellString = f"is authorized to withdraw {total_multi_form_response['Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD) - Quantity' ]}KL of water from borewells." # {{X}}KL of water from {{Y}} borewells. "
            else:
                borewellString = f"Currently, the plant is authorized to withdraw {total_multi_form_response['Quantity of Raw water drawn from the Bore well (Groundwater) (in KLD) - Quantity' ]}KL of water from borewells." # {{X}}KL of water from {{Y}} borewells. "
            
        executiveSummary = f"""
        <h1>Executive Summary</h1>
        <p>This comprehensive report endeavors to outline the water distribution system and usage at {company_name} located at {company_response[0]["Address"]}, {company_response[0]["City"]}, {company_response[0]["State"]} - {company_response[0]["Pincode"]}. Spanning an extensive area of approximately {{xyz}} square meters, {company_name}'s plant exemplifies its leadership in the {company_type} industry.</p>
        <p>Highlighted within this report are the primary water sources, storage facilities, distribution patterns, consumption areas, wastewater treatment facilities, effluent treatment facilities, and rainwater harvesting facilities at the establishment. Moreover, it elucidates the available water-saving opportunities, along with a set of recommendations aimed at enhancing water use efficiency. The report also includes the baseline water balance of the facility and the ideal water balance that the company can achieve by adopting various recommended water conservations. </p>

        <p>This report stems from a thorough water audit conducted by {{WA Company Name}} at the premises of {company_name}, {company_response[0]["City"]}, from {{Date}} to {{Date}}.</p>        

        <h2>About the Company</h2>
        <p>{{About the Company}}</p>
        <p>{{About the location where its situated and its accessibility}}</p>

        <p>
        {company_name}, {company_response[0]["City"]} {tankerString} {borewellString} A significant portion of this water, {{Water Used for Plant Operations}}, is allocated for operational needs, with domestic consumption accounting for the majority. The remaining water finds utility across various functions within the establishment.
        </p>
        <p>Additionally, {company_name}, {company_response[0]["City"]}, secures {total_multi_form_response["Quantity of Raw water drawn (Bulk water supplied) from BWSSB main (in KLD) - Quantity"]}KL of water daily from a district water supply plant. Moreover, the facility procures {filtered_form_response["Quantity of Bottled water supplied from the vendor for potable/ drinking purpose (in KLD)"]} KLD of bottled water exclusively for potable purposes. To further augment water resources, rooftop rainwater harvesting facilities have been operationalized, yielding {filtered_form_response["Approximate total volume of Rainwater collected/ harvested during monsoon season (in KL)"]} KL of water during the monsoon season. This harvested rainwater supplements non-domestic water usage within the premises.</p>
        
        <p>Given the absence of groundwater extraction structures, groundwater usage is not envisaged for any purpose.</p>

        <p>The factory premises host {{Number of RO Plants}} RO plant(s) equipped with {{Number of Pumps}} pumps ({{P}} working and {{Q}} standby), providing softened water for industrial processes. During the audit, it was observed that approximately {{Amount of RO Water Treated}} of water underwent treatment, with an associated rejection rate of about {{Amount of RO Reject}}.</p>
        
        <p>Industrial wastewater generated within the plant is treated via an ETP with a capacity of {{ETP Capacity}}, followed by discharge to the appropriate outlet. Sewage is treated in an STP with a capacity of {{P}}KLD, and the treated effluent is utilized accordingly. Similarly, RO reject and backwash water are redirected for specific purposes.
</p>
        
<p>The major water-consuming areas identified include {{R}}, accounting for {{X}}% of total consumption, and {{P}} plants, accounting for {{Y}}% of total consumption. System losses are quantified at {{Z}}% of total consumption.</p>
<p>{{Water Situation of the Area}}</p>
<p>{{Conclusion/Reason for Necessity of Water Audit}}</p>


        """

        introductionString = f"""
        <h3>1.2.1 Water Supply and Usage Study</h3>
        <p>The first step in a water audit is to conduct a thorough study of water supply and usage within the facility. This entails mapping out water sources, distribution networks, and service points to water users. Flow measurement devices are installed at strategic points to accurately calculate water consumption across various activities. It is crucial to monitor water quality regularly to ensure compliance with safety standards and identify potential contaminants. </p>
        <p>{{Wa company name}} conducted an in-depth analysis of water supply and usage at {company_name} in {company_response[0]["City"]}. This study aimed to comprehend the current water utilization pattern and forecast future requirements. Additionally, {{WA company name}} assessed the viability of sustainable water sources, including rainwater harvesting and wastewater recycling, to enhance {company_name}'s water management practices.

        <h3>1.2.2 Process Analysis</h3>
        <p>Process analysis involves evaluating the efficiency of water usage in different activities and sectors within the facility.  Check for flow measurement devices installed at critical points needs to be carried out to track water consumption accurately. This step also includes checking for daily water quality monitoring. It is necessary to look at the reports to detect any deviations from standards and ensure the integrity of the distribution system. Evaluating the operational efficiency and maintenance levels of water use systems helps in identifying areas for improvement and optimization.</p>

        <p>{{WA company name}} reviewed the flowmeters installed at critical points like {{location of flowmeter to be put in input form}} at {company_name}. The audit team also reviewed the water quality reports. {{insights on water quality reports for company auditor form}}.</p>
        
        <p>{company_name} conducted a comprehensive survey involving outflow, pressure, and power measurements of the current 
        """
        if total_multi_form_response.get("Capacity of the RO Plants installed (in KL) - Capacity", 0) > 0:
            introductionString += f"""
                RO plant, raw water inlet and outlet, as well as wastewater inlet and outlet. This analysis aimed to determine the total water supplied to various sections of the establishment, thereby gaining insights into the volume of water received from the source and distributed to the usage areas.</p>
            """
        else:
            introductionString += f"""
                raw water inlet and outlet, as well as wastewater inlet and outlet. This analysis aimed to determine the total water supplied to various sections of the establishment, thereby gaining insights into the volume of water received from the source and distributed to the usage areas.</p>
            """

        introductionString += f"""
            <p>{{if the premise is ZLD}} The premise has been designed as zero discharge units with recycling of treated water for various uses. </p>

            <h3>1.2.3 System Audit</h3>
            <p>The system audit focuses on assessing the overall performance and integrity of the water distribution system. This includes studying water usage under various sectors such as buildings, plantation, dust suppression, and domestic water supply. Measurement methodologies are verified periodically to ensure accuracy and efficiency. Bulk metering is conducted at the source to identify areas of undue water wastage, while revenue metering helps in monitoring consumption patterns. The audit also examines the potential for wastewater recycling and the recovery of valuable by-products and potential leaks.</p>
            <p>{{WA company name}} conducted a thorough physical examination of the water distribution network/system, including the raw water sources, supply lines to different sections of the establishment, gardens, wastewater treatment plant, combined/individual ETP/STP  treatment plant, canteen, and washrooms. This inspection aimed to determine the daily drinking and domestic water usage in {company_name}'s premises, ultimately facilitating the calculation of per capita water consumption.</p>
        
            <h3>1.2.4 Identify Improvement Opportunities</h3>
            <p>Based on the findings of the water audit, organizations can identify opportunities for improving water efficiency and reducing consumption. This may include implementing water recycling systems, prioritizing water efficiency purchases, and setting realistic reduction goals. Collaboration with the sustainability head of the company is essential for developing best management practices (BMPs) and communicating conservation goals to employees and stakeholders.</p>

            <h3>1.2.5 Combine with Sustainability Certification</h3>
            <p>Integrating water management plans with sustainability certification programs enhances overall sustainability performance. These programs outline short and long-term green initiatives, enabling companies to continually improve and achieve cost savings. By combining water audit findings with sustainability certifications, organizations can demonstrate their commitment to environmental stewardship and social responsibility.</p>

            <h3>1.2.6 Water Saving Strategies</h3>
            <p>Extending the benefits of a water audit involves implementing water-saving strategies across the organization. Regular metering and maintenance ensure proactive management of water conservation goals, while advanced metering infrastructure (AMI) enables real-time monitoring of water usage data. Additionally, exploring water reuse opportunities, such as rainwater harvesting and greywater recycling, further enhances conservation efforts and reduces reliance on freshwater sources.</p>
            <p>{company_name}’s water audit report outlines the various water conservation methods that can be undertaken based on the company's water balance, economic and implementation feasibility studies.</p>
        """

        scope_of_work = f'{{Wa company name}} was given the responsibility to conduct water audit for {company_name} based on the defined scope of work above and then creating this extensive water audit report. '
        # return render_template('auditor/reportTest.html', company_response=company_response, total_multi_form_response=total_multi_form_response)
        return render_template('auditor/report.html', company=company_name, executiveSummary=executiveSummary, introductionString=introductionString, scope_of_work=scope_of_work)
    else:
        # Redirect to the login page if user is not authenticated
        return redirect(url_for('auditor_auth.login_page'))
