import csv
import json
import os

def csv_to_json(csv_file):

  with open(csv_file, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    data = []

    for row in reader:
      json_object = {
        "messages": [
          {
                "role": "system",
                "content": "You are an expert in labeling the content comparison of the Data Safety and Privacy Policy for an Android application."
            },
            {
                "role": "user",
                "content": '''Based on the content of the Data Safety and Privacy Policy. Please label according to the following rule:\n>Label 1: Incorrect if the content is mentioned in Data Safety but not in the Privacy Policy. Correct if the content is mentioned in both documents.\n>Label 2: Incomplete if the content is mentioned in Data Safety but not in the Privacy Policy. Complete if the content is mentioned in both documents.\nThe contents of the two documents are below.\n>Data Safety: '''+ row['data_safety_content'] +'''\n>Privacy Policy:\n''' + row['privacy_policy_content'] +''' \nNote: The shortest answer and no explanation needed, in the format: {label 1: Incorrect or Correct, label 2: Incomplete or Complete}'''
            },
            {
                "role": "assistant",
                "content": '''{label 1:''' + row['label_one_s'] +''', label 2: ''' + row['label_two_s'] +'''}'''
            }
        ],
      }

      data.append(json_object)

  dir_path = '../conf-llm-nlp/data/phase-01/'
  os.makedirs(dir_path, exist_ok=True) 
  with open(os.path.join(dir_path, '100-test.json'), 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4)


csv_file = 'D:\\LLM_Research\\conf-llm-nlp\\data\\phase-01\\200.csv'
csv_to_json(csv_file)

print("JSON file '100-test.json' created successfully.")