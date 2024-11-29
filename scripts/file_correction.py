
import os
import json
import re
import time
import pandas as pd
import google.generativeai as genai
import shutil

from utils.validate_files import test_files

os.makedirs('processed_files', exist_ok=True)

GEMINI_ACCESS_TOKEN = os.getenv('GEMINI_ACCESS_TOKEN')
MAX_RETRIES = 4
DELAY = 4

files_dict = {
    "biens": "data_to_format/biens.json",
    "communes": "data_to_format/communes.json",
    "inspections": "data_to_format/inspections.json", 
    "sections": "data_to_format/sections.json",
    "t_activite": "data_to_format/t_activite.json", 
    "t_contribuable": "data_to_format/t_contribuable.json",
    "t_contribuable_type": "data_to_format/t_contribuable_type.json",
    "t_contribuable_regime": "data_to_format/t_contribuable_regime.json",
    "t_etablissement": "data_to_format/t_etablissement.json", 
    "t_etablissement_activite": "data_to_format/t_etablissement_activite.json",
    "t_etablissement_type": "data_to_format/t_etablissement_type.json",
    "t_poste_comptable": "data_to_format/t_poste_comptable.json",
    "t_structure_region": "data_to_format/t_structure_region.json", 
    "villes": "data_to_format/villes.json"
}


def get_prompt(line):
    return f"""
        ```
        {line} 
        ```

        Where convert this above string to proper json, output format should be only the converted json, no extra strings.
    """


def check_the_line_with_gemini(line):
    attempt = 0
    while attempt < 2:
        try:
            prompt = get_prompt(line)
            genai.configure(api_key=GEMINI_ACCESS_TOKEN)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content([prompt])
            response_text = response.text
            json_text = response_text.split('\n', 1)[-1].strip()

            if json_text:
                json_data = json.loads(json_text.replace("```json", "").replace("```", ""))
                return json_data
            
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {DELAY} seconds...")
            attempt += 1
            time.sleep(DELAY)


def check_json_loads(data):
    try:
        return json.loads(data)
    except Exception as e:
        return False


def check_json_using_pandas(file_path):
    try:
        pd.read_json(file_path)
        return True
    except Exception as e:
        return False

def create_corrected_files(folder_name, filename, file_path=None, list_data=None):
    fn = folder_name+"/"+filename+".json"
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    if file_path:
        shutil.copy(file_path, fn)
    if list_data:
        with open(fn, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(list_data))

    
    print(fn, "File is created")


def generate_file(folder_name):
    for filename, file_path in files_dict.items():
        if check_json_using_pandas(file_path):
            create_corrected_files(folder_name, filename, file_path = file_path)
        else:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                lines = file.readlines()
            if lines:
                if 'results' in lines[0]:
                    create_corrected_files(folder_name, filename, file_path = file_path)
                    continue
                else:
                    lines[0] = lines[0].replace(',', '{')
            with open(file_path, 'w', encoding='ISO-8859-1') as file:
                file.writelines(lines)  

            if check_json_using_pandas(file_path):
                create_corrected_files(folder_name, filename, file_path = file_path)

            else:
                with open(file_path, 'r', encoding='ISO-8859-1') as file:
                    output_data = []
                    wrong_data = []
                    for i, line in enumerate(file):
                        cur_line = line.strip()
                        if i > 2:
                            json_line = cur_line.replace(',{"', '{"')
                            if check_json_loads(json_line):
                                output_data.append(cur_line)
                            if cur_line:
                                data = re.sub(r',\d+,', ',', json_line)
                                if check_json_loads(data):
                                    output_data.append(',' + data)
                                else:
                                    output_data.append(data)
                        else:
                            output_data.append(cur_line)

                create_corrected_files(folder_name, filename, list_data = output_data)
                if wrong_data:
                    create_corrected_files(folder_name, filename+" wrong", list_data = wrong_data)




def main():
    print("File correction is started ...")
    folder_name = input("Write a folder name ")
    
    generate_file(folder_name)
    print("--------------------------")
    print("👐 Testing the created files..")
    test_files(folder_name)


if __name__ == '__main__':
    main()
