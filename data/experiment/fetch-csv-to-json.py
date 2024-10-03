import csv
import json
import os

def sanitize(text):
    """Sanitize the text by replacing special characters if needed."""
    if text is None:
        return ""
    return text.replace("\n", " ").replace("\"", "'")

def csv_to_json(csv_file):
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []

            for row in reader:
                # Sanitize the fields to avoid issues with special characters
                data_safety_content = sanitize(row.get('data_safety_content', ''))
                privacy_policy_content = sanitize(row.get('privacy_policy_content', ''))
                label_one = sanitize(row.get('label_one_s', ''))
                label_two = sanitize(row.get('label_two_s', ''))

                json_object = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert in labeling the content comparison of the Data Safety and Privacy Policy for an Android application."
                        },
                        {
                            "role": "user",
                            "content": '''Based on the content of the Data Safety and Privacy Policy. Please label according to the following rule:\n>Label 1: Incorrect if the content is mentioned in Data Safety but not in the Privacy Policy. Correct if the content is mentioned in both documents.\n>Label 2: Incomplete if the content is mentioned in Data Safety but not in the Privacy Policy. Complete if the content is mentioned in both documents.\nThe contents of the two documents are below.\n>Data Safety: ''' + data_safety_content + '''\n>Privacy Policy:\n''' + privacy_policy_content + ''' \nNote: The shortest answer and no explanation needed, in the format: {label 1: Incorrect or Correct, label 2: Incomplete or Complete}'''
                        },
                        {
                            "role": "assistant",
                            "content": '''{label 1:''' + label_one + ''', label 2: ''' + label_two + '''}'''
                        }
                    ],
                }

                data.append(json_object)

        # Define the output directory and file
        dir_path = '../conf-llm-nlp/data/phase-01/'
        os.makedirs(dir_path, exist_ok=True)

        # Write the JSON file
        json_file_path = os.path.join(dir_path, '100-test.json')
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)

        print(f"JSON file '{json_file_path}' created successfully.")

    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the CSV file path
csv_file = 'D:\\LLM_Research\\conf-llm-nlp\\data\\phase-01\\200.csv'
csv_to_json(csv_file)
