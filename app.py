from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import uuid
import gspread
import pandas as pd
import re
import database
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


load_dotenv()
HACKATHON_COL = os.getenv('HACKATHON_COL', 'Hackathon Name')
TEAM_MEMBERS_COL = os.getenv('TEAM_MEMBERS_COL', 'Team Members')

@app.route('/')
def index():
    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    is_connected = database.check_db_connection()

    if request.method == 'POST':
        print("DEBUG FORM DATA:", request.form)
        hackathon_name = request.form.get('hackathon_name')
        team_members = request.form.get('team_members')
        if hackathon_name and team_members:
          
          # Generate a unique ID for the entry
          unique_id = str(uuid.uuid4())

          # Get current timestamp
          timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

          database.append_new_entry(unique_id, hackathon_name, team_members, timestamp)

          print(f"New Entry: ID={unique_id}, Hackathon={hackathon_name}, Team Members={team_members}, Timestamp={timestamp}")

          return render_template('signup_success.html')
        else:
            error_msg = "Please fill in all required fields."
            return render_template('signup.html', error=error_msg, db_status=is_connected)

    return render_template('signup.html', db_status=is_connected)

@app.route('/participants', methods=['GET'])
def participants():
   
    is_connected = database.check_db_connection()
    df = database.get_all_data()
    
    
    # Simple logic for analysis/display (will need a dropdown for filtering in final version)
    
    unique_hackathons = df[HACKATHON_COL].unique().tolist() if not df.empty else []
    selected_hackathon = request.args.get('hackathon')
    
    participants_df = df 
    unique_participants_list = []
    
    if selected_hackathon:
        # Filter for the selected hackathon
        participants_df = df[df[HACKATHON_COL] == selected_hackathon]
        
        # ANALYSIS: Extract unique individual names
        all_participants = []
        for team_string in participants_df[TEAM_MEMBERS_COL]:
            if isinstance(team_string, str) and team_string.strip():
                members = [re.sub(r'[^\w\s-]', '', name).strip() for name in team_string.split(',')]
                all_participants.extend(members)
        unique_participants_list = sorted(list(set(p for p in all_participants if p)))

    # Pass the DataFrame rows (as a list of lists) and analysis results to the template
    entries = participants_df.values.tolist() if not participants_df.empty else []
    
    return render_template('participants.html', 
                           db_status=is_connected,
                           title='View Entries', 
                           entries=entries,
                           selected_hackathon=selected_hackathon,
                           unique_hackathons=unique_hackathons,
                           unique_participants_list=unique_participants_list)

# -----------------------------------------------------
# 4. Delete Entry Route (MOCK DATA DELETE)
# -----------------------------------------------------

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    id_to_delete = request.form.get('unique_id')
    if(database.delete_entry_by_id(id_to_delete)):
        return redirect(url_for('participants', delete_success='true'))
    else:
        return redirect(url_for('participants', delete_error='Some Error Occurred'))

if __name__ == '__main__':
    app.run(debug=True)