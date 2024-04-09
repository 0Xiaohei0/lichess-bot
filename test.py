import requests

def call_endpoint():
    url = 'http://localhost:8000/'  # Adjust the URL based on your server setup
    data = {'key': 'value'}  # Replace this with the actual data you want to send

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Successfully called the endpoint.")
        else:
            print(f"Failed to call the endpoint. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error calling the endpoint: {e}")

# Call the function to make the request
call_endpoint()
