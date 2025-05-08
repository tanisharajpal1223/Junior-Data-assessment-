from flask import Flask, request, jsonify, render_template
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Ensure the Flask app is defined at the top
app = Flask(__name__)

print('Flask running')

# Database connection details
db_name = "healthcare_db"
user = "neondb_owner"
password = "npg_fT7BkJdyptG0"
host = "ep-proud-wildflower-a8k5dh09-pooler.eastus2.azure.neon.tech"
port = "5432"
# Configure your database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

# Route to display the form
@app.route('/')
def index():
    return render_template('submit_patient.html')  # Make sure this file is inside the 'templates' folder

@app.route('/submit_patient', methods=['POST'])
def submit_patient():
    data = request.form

    # Get the next patient_id from basic_info table
    with engine.connect() as conn:
        result = conn.execute("SELECT patient_id FROM basic_info ORDER BY CAST(SUBSTRING(patient_id, 2) AS INTEGER) DESC LIMIT 1;")
        last_id = result.scalar() or 'P0'
        next_id_number = int(last_id[1:]) + 1
        new_patient_id = f'P{next_id_number}'

    # ========== 1. Insert into basic_info ==========
    basic_info = {
        'patient_id': new_patient_id,
        'ht': data['ht'],
        'wt': data['wt'],
        'education': data['education'],
        'income': data['income'],
        'ageatmenarche': data['ageatmenarche'],
        'ageatmarriage': data['ageatmarriage'],
        'ageatfirstpregnancy': data['ageatfirstpregnancy'],
        'district': data['district'],
        'village': data['village'],
        'occupation': data['occupation'],
        'diet': data['diet'],
        'condition': data['condition']
    }
    pd.DataFrame([basic_info]).to_sql('basic_info', engine, schema='public', if_exists='append', index=False)

    # ========== 2. Insert into delivery_info ==========
    delivery_info = {
        'patient_id': new_patient_id,
        'dateofdelivery': data['dateofdelivery'],
        'ageatdelivery': data['ageatdelivery'],
        'weightatdelivery': data['weightatdelivery'],
        'haemoglobinatdelivery': data['haemoglobinatdelivery'],
        'placentalweight': data['placentalweight'],
        'termofdelivery': data['termofdelivery'],
        'typeofdelivery': data['typeofdelivery']
    }
    pd.DataFrame([delivery_info]).to_sql('delivery_info', engine, schema='public', if_exists='append', index=False)

    # ========== 3. Insert into followup_data ==========
    followup_data = {
        'patient_id': new_patient_id,
        'visit1_bpdis': data['visit1_bpdis'],
        'visit1_bpsys': data['visit1_bpsys'],
        'visit1_date': data['visit1_date'],
        'visit1_wt': data['visit1_wt'],
        'visit2_bpdis': data['visit2_bpdis'],
        'visit2_bpsys': data['visit2_bpsys'],
        'visit2_date': data['visit2_date'],
        'visit2_wt': data['visit2_wt'],
        'visit3_bpdis': data['visit3_bpdis'],
        'visit3_bpsys': data['visit3_bpsys'],
        'visit3_date': data['visit3_date'],
        'visit3_wt': data['visit3_wt'],
        'visit4_bpdis': data['visit4_bpdis'],
        'visit4_bpsys': data['visit4_bpsys'],
        'visit4_date': data['visit4_date'],
        'visit4_wt': data['visit4_wt']
    }
    pd.DataFrame([followup_data]).to_sql('followup_data', engine, schema='public', if_exists='append', index=False)

    return jsonify({'status': 'success', 'patient_id': new_patient_id})

# Ensure the app runs correctly when executed
if __name__ == '__main__':
    app.run(debug=True)
