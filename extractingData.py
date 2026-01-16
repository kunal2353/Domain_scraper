import requests
import pandas as pd
from pandas.errors import EmptyDataError

url = "https://companyenrichment.abstractapi.com/v2/"

params = {
    "api_key": "f554e842296e44ea9c532655a2656377",
    "domain": "airbnb.com"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    df_new = pd.DataFrame([data])

    file_name = "company_data.csv"

    try:
        df_existing = pd.read_csv(file_name)

        df_final = pd.concat([df_existing, df_new], ignore_index=True)

        df_final.drop_duplicates(subset=["domain"], keep="first", inplace=True)

    except (FileNotFoundError, EmptyDataError):
        # File missing OR empty
        df_final = df_new

    df_final.to_csv(file_name, index=False)

    print("✅ Data saved successfully (duplicates handled)")

else:
    print("Error:", response.status_code, response.text)
