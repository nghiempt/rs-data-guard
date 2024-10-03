import csv
import os

def csv_to_csv(csv_file, output_csv):

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        with open(output_csv, 'w', newline='', encoding='utf-8') as outcsv:
            fieldnames = ['Id', 'Context', 'Question', 'Answer']
            writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
            writer.writeheader()

            count = 0

            for row in reader:
                context = "You are an expert in labeling the content comparison of the Data Safety and Privacy Policy for an Android application."
                
                question = f'''Based on the content of the Data Safety and Privacy Policy. Please label according to the following rule:\n>Label 1: Incorrect if the content is mentioned in Data Safety but not in the Privacy Policy. Correct if the content is mentioned in both documents.\n>Label 2: Incomplete if the content is mentioned in Data Safety but not in the Privacy Policy. Complete if the content is mentioned in both documents.\nThe contents of the two documents are below.\n>Data Safety: {row['data_safety_content']}\n>Privacy Policy:\n{row['privacy_policy_content']} \nNote: The shortest answer and no explanation needed, in the format: {{label 1: Incorrect or Correct, label 2: Incomplete or Complete}}'''

                answer = f"{{label 1: {row['label_one_s']}, label 2: {row['label_two_s']}}}"

                writer.writerow({
                    'Id': row['app_id'],  # Assuming 'app_id' is the ID column
                    'Context': context,
                    'Question': question,
                    'Answer': answer
                })
                count+=1

    print(f"CSV file '{output_csv}' created successfully.")

csv_file = 'D:\\LLM_Research\\conf-llm-nlp\\data\\phase-01\\200.csv'
output_csv = 'D:\\LLM_Research\\conf-llm-nlp\\data\\phase-01\\50-samples.csv'

csv_to_csv(csv_file, output_csv)
