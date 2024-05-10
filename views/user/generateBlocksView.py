def generate_blocks_view(blocks_response, company_id):
    # Start building the HTML table
    html_table = "<table border='1'>"

    # Add table headers
    html_table += "<tr>"
    html_table += "<th>Name</th>"
    html_table += "<th>Length</th>"
    html_table += "<th>Width</th>"
    html_table += "<th>Roof Area</th>"
    html_table += "<th>Surface Type</th>"
    html_table += "</tr>"

    # Add table rows
    for block in blocks_response:
        if company_id == block['Company ID']:
            html_table += "<tr>"
            html_table += f"<td>{block['Name']}</td>"
            html_table += f"<td>{block['Length']}</td>"
            html_table += f"<td>{block['Width']}</td>"
            html_table += f"<td>{block['Roof Area']}</td>"
            html_table += f"<td>{block['Surface Type']}</td>"
            html_table += "</tr>"

    # Close the table
    html_table += "</table>"

    return html_table

