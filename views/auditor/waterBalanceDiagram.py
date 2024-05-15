from flask import Blueprint, request, render_template
import requests

auditor_balance_diagram = Blueprint('auditor_balance_diagram', __name__)



@auditor_balance_diagram.route('/auditor/water-balance-diagram', methods=['GET'])
def generate_balance_diagram():
    return render_template('auditor/waterBalanceDiagram.html')
