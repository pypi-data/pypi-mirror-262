import argparse
import os
from x_code.core import get_response

# Function to prompt the user for the endpoint URL and store it for future use
def prompt_for_endpoint_url():
    endpoint_url = input("Enter the new endpoint URL: ")
    # Save endpoint URL to a configuration file or environment variable
    with open(os.path.expanduser("~/.x_config"), "w") as config_file:
        config_file.write(endpoint_url)
    print(f"Endpoint URL updated to: {endpoint_url}")

def main():
    parser = argparse.ArgumentParser(description="Interact with the endpoint.")
    parser.add_argument("question", nargs="?", help="Specify the question to send to the endpoint.")
    parser.add_argument("file_path", nargs="?", help="Specify the path to the file.")
    parser.add_argument("--endpoint-url", action="store_true", help="Get the existing endpoint URL.")
    parser.add_argument("--change-endpoint", action="store_true", help="Change the endpoint URL.")
    parser.add_argument("--remove-endpoint", action="store_true", help="Remove the stored endpoint URL.")
    args = parser.parse_args()

    # If --endpoint-url option is provided, print the existing endpoint URL
    if args.endpoint_url:
        config_file_path = os.path.expanduser("~/.x_config")
        if os.path.exists(config_file_path):
            with open(config_file_path, "r") as config_file:
                endpoint_url = config_file.read().strip()
            print(f"Current Endpoint URL: {endpoint_url}")
        else:
            print("Endpoint URL not set.")
        return

    # If --change-endpoint option is provided, prompt the user to enter a new endpoint URL
    if args.change_endpoint:
        prompt_for_endpoint_url()
        return

    # If --remove-endpoint option is provided, remove the stored endpoint URL
    if args.remove_endpoint:
        config_file_path = os.path.expanduser("~/.x_config")
        if os.path.exists(config_file_path):
            os.remove(config_file_path)
            print("Endpoint URL removed.")
        else:
            print("Endpoint URL not set.")
        return

    # Check if endpoint URL is stored in configuration file
    endpoint_url = None
    config_file_path = os.path.expanduser("~/.x_config")
    if os.path.exists(config_file_path):
        with open(config_file_path, "r") as config_file:
            endpoint_url = config_file.read().strip()

    # If endpoint URL is not stored, prompt the user to enter it
    if not endpoint_url:
        prompt_for_endpoint_url()
        # Read endpoint URL from the configuration file
        with open(config_file_path, "r") as config_file:
            endpoint_url = config_file.read().strip()

    # If both question and file path are provided, read file content
    if args.file_path:
        # Read file content
        with open(args.file_path, 'r') as file:
            file_content = file.read()

        # Append file content to the question
        question = f"{args.question}\n\nFile Content:\n{file_content}"
    else:
        question = args.question

    # Send the modified question to the endpoint
    response = get_response(question, endpoint_url)
    print(response)

if __name__ == "__main__":
    main()

