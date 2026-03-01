import requests
import pandas as pd
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Working"

@app.route("/run")
def run():
    try:
        data = requests.get("https://mun-dat.onrender.com/registrations")
        df = pd.DataFrame(data.json())

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        creds_path = os.path.join(BASE_DIR, "something.json")

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            creds_path, scope
        )

        client = gspread.authorize(creds)
        sheet = client.open("MUN_Registrations").sheet1

        set_with_dataframe(sheet, df)

        return "<a href='https://docs.google.com/spreadsheets/d/1jOBWzZ54qjeUrcsDbVlm7tTx1MBqEfhm6ZNREy6rlVE/edit?gid=0#gid=0'>Link to Google Sheets</a>"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)