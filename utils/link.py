import requests

def resolve_google_maps_link(shortened_url):
    try:
        response = requests.head(shortened_url, allow_redirects=True)
        full_url = response.url
        return full_url
    except Exception as e:
        return f"Error resolving link: {str(e)}"
    
def extract_place_name(full_url):
    if "/place/" in full_url:
        start = full_url.find("/place/") + len("/place/")
        end = full_url.find("/", start)
        place_name = full_url[start:end].replace("+", " ")
        return place_name
    return None