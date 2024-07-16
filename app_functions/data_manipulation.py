import yaml
import pandas as pd

def read_config(build=False):
    # Load config file
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Please create a config.yaml file in the directory of the driver.")
        exit(1)

    try:
        api_token = config["api_token"]
    except KeyError:
        print("API token not found in config file. Please add an 'api_token' field.")
        exit(1)

    if build:
        return api_token

    # list of sports is exhaustive and will exhaust api limit, user must specify sports
    try:
        sports = config["sports"]

    except KeyError:
        print("Sports list not found in config file. Please add a 'sports' field.")
        exit(1)

    # user can choose to not specify bookmakers
    bookmakers = config.get("bookmakers", None)

    # build config dictionary
    config = {
        "api_token": api_token,
        "sports": sports,
        "bookmakers": bookmakers
    }
    return config

def json_to_df(json_data):
    # create df with columns
    df = pd.DataFrame(columns=["sport", "bookmaker", "bet type", "event date", "favorite", "underdog", "odds favorite", "odds underdog"])

    for set in json_data:
        for event in set:
            # get sport
            sport = event["sport_title"]
            bookmakers = event["bookmakers"]
            date = event["commence_time"].split("T")[0]
            
            for bookmaker in bookmakers:
                bookie = bookmaker["key"]
                markets = bookmaker["markets"]

                for market in markets:
                    bet_type = market["key"]
                    outcomes = market["outcomes"]
                    
                    # will only consider bets with 2 outcomes
                    if len(outcomes) == 2:
                        outcome1 = outcomes[0]
                        outcome2 = outcomes[1]

                        outcomeOdds1 = outcome1["price"]
                        outcomeOdds2 = outcome2["price"]

                        # determine favorite and underdog
                        if outcomeOdds1 < outcomeOdds2:
                            favorite = outcome1["name"]
                            underdog = outcome2["name"]
                            odds_favorite = outcomeOdds1
                            odds_underdog = outcomeOdds2
                        else:
                            favorite = outcome2["name"]
                            underdog = outcome1["name"]
                            odds_favorite = outcomeOdds2
                            odds_underdog = outcomeOdds1
                        
                        # append to df
                        new_index = len(df)
                        df.loc[new_index] = {
                            "sport": sport,
                            "bookmaker": bookie,
                            "bet type": bet_type,
                            "event date": date,
                            "favorite": favorite,
                            "underdog": underdog,
                            "odds favorite": odds_favorite,
                            "odds underdog": odds_underdog
                        }

        return df   