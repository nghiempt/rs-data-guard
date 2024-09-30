import asyncio
import csv
import os
import json
import aiohttp
from dotenv import load_dotenv

class HANDLER:
    @staticmethod
    def remove_empty_lines(content):
        lines = content.split("\n")
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)

    @staticmethod
    async def call_api_student(data_safety_content, privacy_policy_content):
        url = "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
            "Content-Type": "application/json"
        }

        # Payload in the format provided by Postman
        payload = json.dumps({
            "model": "microsoft/Phi-3-mini-4k-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in labeling the content comparison of the Data Safety and Privacy Policy for an Android application."
                },
                {
                    "role": "user",
                    "content": f"Based on the content of the Data Safety and Privacy Policy. Please label according to the following rule:\n> Label 1: Incorrect if the content is mentioned in Data Safety but not in the Privacy Policy. Correct if the content is mentioned in both documents.\n> Label 2: Incomplete if the content is mentioned in Data Safety but not in the Privacy Policy. Complete if the content is mentioned in both documents.\nThe contents of the two documents are below.\n> Data Safety: {data_safety_content}\n> Privacy Policy: {privacy_policy_content}\nNote: The shortest answer and no explanation needed, in the format: {{label 1: Incorrect or Correct, label 2: Incomplete or Complete}}"
                }
            ],
            "max_tokens": 1000,
            "stream": False
        })

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                # Check if the response content type is JSON
                if response.headers['Content-Type'] == 'application/json':
                    response_json = await response.json()
                    if 'error' in response_json:
                        return f"Error: {response_json['error']}"

                    # Extracting the content from the message in choices array
                    content = response_json["choices"][0]["message"]["content"]
                    return content
                else:
                    # If not JSON, read the response as text
                    response_text = await response.text()
                    return f"Unexpected response: {response_text}"

    @staticmethod
    async def loop_csv(input_csv_path, output_csv_path):
        with open(input_csv_path, "r", newline="", encoding="utf-8") as csvfile, open(
            output_csv_path, "w", newline="", encoding="utf-8"
        ) as outputfile:

            reader = csv.reader(csvfile)
            writer = csv.writer(outputfile)

            headers = next(reader)
            writer.writerow(headers)

            for index, row in enumerate(reader):
                print(f"\n_____________ Run times {index + 1} <{row[0]}> _____________")
                
                # Extracting required data
                app_id = row[0]
                app_pkg = row[1]
                data_safety_content = row[3]
                privacy_policy_content = row[4]

                # Asynchronous API call
                assistant_reply = await HANDLER.call_api_student(data_safety_content, privacy_policy_content)

                # Check for errors in the API response and write to CSV
                if "Error" in assistant_reply:
                    writer.writerow([app_id, app_pkg, data_safety_content, privacy_policy_content, "Error"])
                else:
                    writer.writerow([app_id, app_pkg, data_safety_content, privacy_policy_content, assistant_reply])
                
                print("~~~~~~~~~~~~~~ Success ~~~~~~~~~~~~~~\n")

async def main():
    load_dotenv()  # Load environment variables from .env file
    input_csv_path = "data/phase-01/200v2.csv" 
    output_csv_path = "output/phase-01/experiment-01/output-student.csv"

    await HANDLER().loop_csv(input_csv_path, output_csv_path)


if __name__ == "__main__":
    asyncio.run(main())
