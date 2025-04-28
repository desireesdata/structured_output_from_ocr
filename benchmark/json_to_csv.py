import pandas as pd
import json

def json_to_csv(json_file: str, csv_file: str):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        entries = data.get("entry", [])
        df = pd.DataFrame(entries)
        required_columns = ["nom", "fonction", "adresse"]
        if not all(column in df.columns for column in required_columns):
            raise ValueError("Le fichier JSON a un probleme")
        df.to_csv(csv_file, sep='\t', index=False, columns=required_columns)

        print(f"Zou: {csv_file}")
    except Exception as e:
        print(f"Erreur : {e}")

json_to_csv('../output/entries_from_ocr.json', 'json_converted.csv')
