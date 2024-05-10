def geenerate_companies_view(companies_data):
    table_html = """
    <table class="table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Type</th>
                <th>Scope Of Work</th>
                <th>Address</th>
                <th>City</th>
                <th>Password</th>
                <th>Form entries</th>
            </tr>
        </thead>
        <tbody>
    """
    for company in companies_data:
        table_html += f"""
            <tr>
                <td>{company['ID']}</td>
                <td>{company['Name']}</td>
                <td>{company['Type']}</td>
                <td>{company['Scope Of Work']}</td>
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
