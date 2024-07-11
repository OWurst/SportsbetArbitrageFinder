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

def get_bookmakers_request(api_token, sport, regions):
    url = "https://api.the-odds-api.com/v4/sports/{sport}/odds"
    params = {
        "api_key": api_token,
        "regions": regions,
        "oddsFormat": "american"
    }

    try:
        response = requests.get(url.format(sport=sport), params=params)

        bookies = set()

        for data in response.json():
            bookmaker_data = data["bookmakers"]
            for bookie in bookmaker_data:
                bookies.add(bookie["key"])

        return bookies
    
    except Exception as e:
        print(f"Error: {e}")
        return set()
