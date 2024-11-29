
import os
import json

def format_the_file(files_dict):
    for file, file_path in files_dict.items():
        if not os.path.isfile(file_path):
            print("File is not exist")
            continue
        with open(file_path, 'r', encoding='ISO-8859-1') as f_data:
            try:
                json.loads(f_data.read())
                print(f"{file} in correct format")
            except Exception:
                print("🔴🔴🔴🔴 File which is not correct format 🔴🔴🔴🔴", file_path)

def test_files(folder_name):
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
    else:
        print("Folder is not exist")

