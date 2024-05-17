def generate_table_view(table_data, prefix=None, dropdown=None, blocks=None):
    # Incrementing the counter to generate a unique ID for each table
    generate_table_view.counter += 1
    table_id = f"table{generate_table_view.counter}"

    # Initialize the HTML string with table structure
    html = "<table id='" + table_id + "'>\n"

    # Reset the counter when it reaches the maximum value (just to be safe)
    if generate_table_view.counter >= 1000000:
        generate_table_view.counter = 0
    
    # Extract column names from the first dictionary in the list
    columns = list(table_data[0].keys()) if prefix is None else [col for col in table_data[0].keys() if col.startswith(prefix)]

    # Add table header row
    html += "<tr>\n"
    for column in columns:
        html += f"<th>{column}</th>\n"
    html += "</tr>\n"
    
    # Filter rows if prefix is specified
    rows = table_data if prefix is None else [row for row in table_data if any(col.startswith(prefix) for col in row.keys())]

    # Add table rows
    for row in rows:
        html += "<tr>\n"
        for column in columns:
            td_value = row.get(column, '')
            if td_value != "":
                html += f"<td contenteditable>{td_value}</td>\n"
        html += "</tr>\n"
    
    # Extract dropdown options from blocks if provided
    dropdown_options = ""
    if blocks and isinstance(blocks, list) and all(isinstance(block, dict) and "Name" in block for block in blocks):
        for block in blocks:
            dropdown_options += f"<option value='{block['Name']}'>{block['Name']}</option>\n"

    # Add empty row with editable cells and dropdown in the first column
    html += f"<tr id='empty-row-{table_id}' style='display:none;'>\n"
    # Add dropdown to the first column if options exist
    if dropdown_options:
        html += f"<td><select>{dropdown_options}</select></td>\n"
    else:
        html += "<td contenteditable></td>\n"
    # Add editable cells to the remaining columns
    for _ in range(len(columns) - 1):
        html += "<td contenteditable></td>\n"
    html += "</tr>\n"

    # Close the table tag
    html += "</table>\n"

    # Add button to add empty row for this specific table
    html += f"<button type='button' onclick='addEmptyRow(\"{table_id}\")'>Add Row</button>\n"

    # JavaScript function to add empty row
    html += """
    <script>
    function addEmptyRow(tableId) {
        var table = document.querySelector('table#' + tableId);
        var newRow = document.getElementById('empty-row-' + tableId).cloneNode(true);
        newRow.removeAttribute('id');
        newRow.style.display = '';
        table.appendChild(newRow);
    }
    </script>
    """

    return html

# Initialize the counter variable
generate_table_view.counter = 0


# def generate_table_view(table_data, prefix=None, dropdown=None, blocks = None):
#     # Incrementing the counter to generate a unique ID for each table
#     generate_table_view.counter += 1
#     table_id = f"table{generate_table_view.counter}"

#     # Initialize the HTML string with table structure
#     html = "<table id='" + table_id + "'>\n"

#     # Reset the counter when it reaches the maximum value (just to be safe)
#     if generate_table_view.counter >= 1000000:
#         generate_table_view.counter = 0
    
#     # Extract column names from the first dictionary in the list
#     columns = list(table_data[0].keys()) if prefix is None else [col for col in table_data[0].keys() if col.startswith(prefix)]

#     # Add table header row
#     html += "<tr>\n"
#     for column in columns:
#         html += f"<th>{column}</th>\n"
#     html += "</tr>\n"
    
#     # Filter rows if prefix is specified
#     rows = table_data if prefix is None else [row for row in table_data if any(col.startswith(prefix) for col in row.keys())]

#     # Add table rows
#     for row in rows:
#         html += "<tr>\n"
#         for column in columns:
#             td_value = row.get(column, '')
#             if td_value == "":
#                 pass
#             else:
#                 html += f"<td contenteditable>{row.get(column, '')}</td>\n"
#         html += "</tr>\n"
    
#     # Add empty row with editable cells
#     html += f"<tr id='empty-row-{table_id}' style='display:none;'>\n"
#     for _ in range(len(columns)):
#         html += "<td contenteditable></td>\n"
#     html += "</tr>\n"

#     # Close the table tag
#     html += "</table>\n"

#     # Add button to add empty row for this specific table
#     html += f"<button onclick='addEmptyRow(\"{table_id}\")'>Add Row</button>\n"

#     # JavaScript function to add empty row
#     html += """
#     <script>
#     function addEmptyRow(tableId) {
#         var table = document.querySelector('table#' + tableId);
#         var newRow = document.getElementById('empty-row-' + tableId).cloneNode(true);
#         newRow.removeAttribute('id');
#         newRow.style.display = '';
#         table.querySelector('tbody').appendChild(newRow);
#     }
#     </script>
#     """

#     return html

# # Initialize the counter variable
# generate_table_view.counter = 0