import json
import os
from tqdm import tqdm

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    # Create parent directories if they don't exist
    dir_path = os.path.dirname(file_path)
    if dir_path:  # Only create directory if path is not empty
        os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def process_str_to_list(file_path, save_path):
    json_data = load_json(file_path)
    for item in tqdm(json_data, desc="Processing JSON data", total=len(json_data)):
        item['ingredients'] = json.loads(item['ingredients'])
        item['directions'] = json.loads(item['directions'])
    save_json(json_data, save_path)

def create_json_subset(file_path, save_path, num_items):
    json_data = load_json(file_path)
    json_data = json_data[:num_items]
    save_json(json_data, save_path)
    return json_data