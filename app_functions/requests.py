import requests

def get_sports_request(api_token):
    url = "https://api.the-odds-api.com/v4/sports"
    params = {
        "api_key": api_token,
        "all": "true"
    }
    response = requests.get(url, params=params)

    sports = set()
    for sport in response.json():
        sports.add(sport["key"])

    return sports
