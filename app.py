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
        data1 = requests.get("https://mun-dat.onrender.com/groups")
        df = pd.DataFrame(data.json())
        df2 = pd.DataFrame(data1.json())

        max_participants = df2["participants"].apply(len).max()

        for i in range(max_participants):
            df2[f"p{i+1}_name"] = df2["participants"].apply(lambda x: x[i]["name"] if len(x) > i else "")
            # df2[f"p{i+1}_phone"] = df2["participants"].apply(lambda x: x[i]["phone"] if len(x) > i else "")
            # df2[f"p{i+1}_email"] = df2["participants"].apply(lambda x: x[i]["email"] if len(x) > i else "")
            df2[f"p{i+1}_preference"] = df2["participants"].apply(lambda x: x[i]["preference"] if len(x) > i else "")
            df2[f"p{i+1}_portfolio1"] = df2["participants"].apply(lambda x: x[i]["portfolio1"] if len(x) > i else "")
            df2[f"p{i+1}_portfolio2"] = df2["participants"].apply(lambda x: x[i]["portfolio2"] if len(x) > i else "")
            df2[f"p{i+1}_ipRole"] = df2["participants"].apply(lambda x: x[i]["ipRole"] if len(x) > i else "")

        df2 = df2.drop(columns=["participants"])

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
        sheet2 = client.open("MUN_Group").sheet1

        set_with_dataframe(sheet, df)
        set_with_dataframe(sheet2, df2)

        return "<a href='https://docs.google.com/spreadsheets/d/1jOBWzZ54qjeUrcsDbVlm7tTx1MBqEfhm6ZNREy6rlVE/edit?gid=0#gid=0'>Link for Individual Registrations</a><br><a href='https://docs.google.com/spreadsheets/d/1lvWxZpEQMb2ujbeEzJ4chdEnicnz5XuZWWRFJC3CZdo/edit?gid=0#gid=0'>Link for Group Registrations</a>"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)