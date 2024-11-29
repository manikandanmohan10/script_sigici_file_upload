
import os
import json
import pandas as pd
from sqlalchemy import create_engine

# engine = create_engine('postgresql://postgres:A!6~4zm1Rl;5>W@54.37.65.120:5432/sigici')
engine = create_engine('postgresql://postgres:strategy%40123@54.37.65.120:5432/sigici_data')


def insert_data(file, df):
    df.to_sql(file, engine, if_exists = 'append', index=False)
    print("Inserted ..")


def process_data(file, items):
    if items:
        df = pd.DataFrame.from_dict(items)
        if 'bien_datcre' in df.columns :
            df['bien_datcre'] = pd.to_datetime(df['bien_datcre'], format='%d/%m/%y', errors='coerce')
        if 'bien_datemod' in df.columns:
            df['bien_datemod'] = pd.to_datetime(df['bien_datemod'], format='%d/%m/%y')
        if 'date_debut_activite' in df.columns:
            df['date_debut_activite'] = pd.to_datetime(df['date_debut_activite'], format='%d/%m/%y')
        if 'date_inscription' in df.columns:
            df['date_inscription'] = pd.to_datetime(df['date_inscription'], format='%d/%m/%y')
        if 'date_creation' in df.columns:
            df['date_creation'] = pd.to_datetime(df['date_creation'], format='%d/%m/%y')
        if 'date_comportement' in df.columns:
            df['date_comportement'] = pd.to_datetime(df['date_comportement'], format='%d/%m/%y')
        if 'date_cessation' in df.columns:
            df['date_cessation'] = pd.to_datetime(df['date_cessation'], format='%d/%m/%y')
        if 'date_migration_sigici' in df.columns:
            df['date_migration_sigici'] = pd.to_datetime(df['date_migration_sigici'], format='%d/%m/%y')
        if 'poste_comptable_id' in df.columns:
            df['poste_comptable_id'] = df['poste_comptable_id'].astype(str)
            df = df.drop('poste_comptable_id', axis=1)
        if 'code_rpi' in df.columns:
            df = df.drop('code_rpi', axis=1)

        insert_data(file, df)


def format_the_file(files_dict):

    for file, file_path in files_dict.items():
        print(f"Processing the {file}")
        if not os.path.isfile(file_path):
            print("File is not exist")
            continue
        with open(file_path, 'r', encoding='ISO-8859-1') as f_data:
            try:
                data_dict = json.loads(f_data.read())
            except Exception as e:
                raise Exception("Please look into this file which has wrong data ", file_path)
                
            if data_dict.get('results'):
                for result in data_dict.get('results'):
                    if result.get('items'):
                        process_data(file, result.get('items'))
            if data_dict.get('items'):
                process_data(file, data_dict.get('items'))


def main():
    print("File correction is started ...")
    # folder_name = input("Write a folder name ")
    folder_name = 'upload_files'
    if os.path.isdir(folder_name):
        files_dict = {
            "communes": f"{folder_name}/communes.json",
            "inspections": f"{folder_name}/inspections.json", 
            "sections": f"{folder_name}/sections.json",
            "t_activite": f"{folder_name}/t_activite.json", 
            "t_contribuable": f"{folder_name}/t_contribuable.json",
            "t_contribuable_type": f"{folder_name}/t_contribuable_type.json",
            "t_contribuable_regime": f"{folder_name}/t_contribuable_regime.json",
            "t_etablissement": f"{folder_name}/t_etablissement.json", 
            "t_etablissement_activite": f"{folder_name}/t_etablissement_activite.json",
            "t_etablissement_type": f"{folder_name}/t_etablissement_type.json",
            "t_structure_region": f"{folder_name}/t_structure_region.json", 
            "villes": f"{folder_name}/villes.json",
            "biens": f"{folder_name}/biens.json",
            "t_poste_comptable": f"{folder_name}/t_poste_comptable.json",
        }

        format_the_file(files_dict)
        print("All done 😃")
    else:
        print("Folder is not exist")


if __name__ == '__main__':
    main()
