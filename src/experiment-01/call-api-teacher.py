import ast
import requests
import os
import json
import csv
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

url = "https://api.openai.com/v1/chat/completions"

# Đọc prompt từ file JSON
def load_prompt(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Định nghĩa hàm extract_privacy_policy_content
def extract_privacy_policy_content(privacy_policy_content):
    data_share = None
    data_collect = None
    if "Data Share:" in privacy_policy_content and "Data Collect:" in privacy_policy_content:
        split_content = privacy_policy_content.split("Data Collect:")
        data_share = split_content[0].replace("Data Share:", "").strip()
        data_collect = split_content[1].strip()
    return data_share, data_collect

def call_api_student(app_pkg, category_name, data_safety_content, privacy_policy_content, prompt):
    data_safety = ast.literal_eval(data_safety_content)  # Chuyển đổi chuỗi JSON thành đối tượng Python
    
    ds_data_share = data_safety.get('data_shared', [])
    ds_data_collected = data_safety.get('data_collected', [])
    ds_security_practices = data_safety.get('security_practices', [])
    
    print(f"ds_data_share: {ds_data_share}")
    print(f"ds_data_collected: {ds_data_collected}")
    print(f"ds_security_practices: {ds_security_practices}")
    
    pp_data_share, pp_data_collect = extract_privacy_policy_content(privacy_policy_content)

    user_prompt = prompt["user"].replace("{ds_data_share}", str(ds_data_share)) \
                                .replace("{ds_data_collected}", str(ds_data_collected)) \
                                .replace("{ds_security_practices}", str(ds_security_practices)) \
                                .replace("{pp_data_share}", pp_data_share if pp_data_share else "N/A") \
                                .replace("{pp_data_collect}", pp_data_collect if pp_data_collect else "N/A")
    print('Prompt: ' + user_prompt)
    payload = {
        "model": "gpt-3.5-turbo", 
        "messages": [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.5 
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": f"Failed to get response for {app_pkg}, status code: {response.status_code}"}


def process_csv_and_call_api(csv_file, prompt):
    results = [] 
    
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            app_pkg = row['app_pkg']
            category_name = row['category_name'] 
            data_safety_content = row['data_safety_content']  
            privacy_policy_content = row['privacy_policy_content']  
            
            print(f"Processing app: {app_pkg}")
            
            api_result = call_api_student(app_pkg, category_name, data_safety_content, privacy_policy_content, prompt)
            results.append({
                "app_pkg": app_pkg,
                "category_name": category_name,
                "api_response": api_result
            })
    
    return results

# Lưu kết quả vào file JSON
def save_results_to_json(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_file}")

csv_file = "data/phase-01/200v2.csv"  

prompt_file = "prompt/phase-01/prompt.json"

prompt = load_prompt(prompt_file)

results = process_csv_and_call_api(csv_file, prompt)

output_file = "output/phase-01/experiment-01/output-teacher.json"
save_results_to_json(results, output_file)
