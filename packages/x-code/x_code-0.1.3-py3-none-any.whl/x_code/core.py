import requests

def get_response(question, endpoint_url, file_path=None):
    try:
        if file_path:
            with open(file_path, 'r') as file:
                file_content = file.read()
            data = {"question": question, "file_content": file_content}
        else:
            data = {"question": question}

        # Send the data to the endpoint URL
        response = requests.post(endpoint_url, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            response_text = data.get("response", "No response received from the endpoint")
            return response_text
        else:
            return f"Request failed with status code: {response.status_code}"
    except Exception as e:
        return f"Error processing request: {str(e)}"

