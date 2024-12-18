import requests
from config.config import Config

def fetch_geoapify_data():
    # Define the API URL and key
    api_url = "https://api.geoapify.com/v1/ipinfo"
    api_key = Config.GEOAPIFY_API_KEY

    # Make the API request
    response = requests.get(api_url, params={"apiKey": api_key})

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant data
        state_name = data.get("state", {}).get("name", "Unknown State")
        country_name = data.get("country", {}).get("name", "Unknown Country")
        currency = data.get("country", {}).get("currency", "Unknown Currency")

        # Update the placeholders or process data
        region_text = f"{state_name}, {country_name}"
        price_placeholder = f"i.e) 25.30 / Price in {currency}"

        return region_text, price_placeholder
    else:
        print(f"Error fetching data: {response.status_code}")
