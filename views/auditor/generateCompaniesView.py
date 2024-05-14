def geenerate_companies_view(companies_data, completed = ''):
    if completed == True:
        completed = '1'
    table_html = """
    <h2>Ongoing Projects</h2>
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Address</th>
                <th>City</th>
                <th>Password</th>
                <th>Form entries</th>
            </tr>
        </thead>
        <tbody>
    """
    for company in companies_data:
        if company["completed"] == '':
            table_html += f"""
                <tr>
                    <td>{company['ID']}</td>
                    <td>{company['Name']}</td>
                    <td>{company['Type']}</td>
                    <td>{company['Address']}</td>
                    <td>{company['City']}</td>
                    <td>{company['pass']}</td>
                    <td> <a href="/auditor/dash?type={company['Type']}&company={company['ID']}&name={company['Name']}"> 
                        <button>Click</button>
                        </a>
                    </td>
                </tr>
            """
    table_html += """
        </tbody>
    </table>

    <h2>Completed Projects </h2>
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Address</th>
                <th>City</th>
                <th>Password</th>
                <th>Form entries</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for company in companies_data:
        if company["completed"] == '1':
            table_html += f"""
                <tr>
                    <td>{company['ID']}</td>
                    <td>{company['Name']}</td>
                    <td>{company['Type']}</td>
                    <td>{company['Address']}</td>
                    <td>{company['City']}</td>
                    <td>{company['pass']}</td>
                    <td> <a href="/auditor/dash?type={company['Type']}&company={company['ID']}&name={company['Name']}"> 
                        <button>Click</button>
                        </a>
                    </td>
                </tr>
            """
    table_html += """
        </tbody>
    </table>
    """
    return table_html
