# x_code

**x_code** is a Python package that provides a command-line interface for interacting with coding assistant.

## Installation

You can install **x_code** via pip:

```bash
pip install x_code

Usage
After installing the package, you can use the x command-line interface (CLI) to interact with the endpoint.

Sending Questions
To send a question to the endpoint, use the following command:

bash
x "your question here"
This will send your question to the endpoint and print the response.

Endpoint URL
You can set the endpoint URL for the package using the --change-endpoint option. If you want to check the existing endpoint URL, you can use the --endpoint-url option. Here's how:

bash
x --change-endpoint
This will prompt you to enter a new endpoint URL. Once you enter the URL, it will be stored for future use.

bash
x --endpoint-url
This will display the existing endpoint URL if it's set.

Removing Endpoint URL
If you want to remove the stored endpoint URL, you can use the --remove-endpoint option:

bash
x --remove-endpoint
This will remove the stored endpoint URL.

Using Specific Endpoint URL
If you want to use a specific endpoint URL for a single command, you can specify it using the --endpoint-url option:

bash
x "your question here" --endpoint-url "http://example.com/endpoint"
This will send your question to the specified endpoint URL.

License
This project is licensed under the MIT License - see the LICENSE file for details.

This README provides comprehensive information about installing, configuring, and using the X package, including all the updates related to managing the endpoint URL.

