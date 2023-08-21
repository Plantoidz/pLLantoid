from dotenv import load_dotenv
import requests
import os
import json

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment
eleven_labs_api_key = os.environ.get("ELEVEN")

# Define the API URL
url = "https://api.elevenlabs.io/v1/voices"

# Set request headers
headers = {
    "Accept": "application/json",
    "xi-api-key": eleven_labs_api_key
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Pretty print the response
    print(json.dumps(data, indent=4))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
