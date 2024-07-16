import pandas as pd
import app_functions.data_manipulation as dm
import app_functions.requests as req

if __name__ == "__main__":
    config = dm.read_config()

    # read sport as sport field in config
    sport = config["sports"]
    token = config["api_token"]
    bookmakers = config["bookmakers"]

    # get odds for each sport
    all_odds = [] 
    for s in sport:
        odds = req.get_odds_request(token, s, bookmakers)
        all_odds.append(odds)

    # convert to dataframe
    df = dm.json_to_df(all_odds)
    print(df.head())
    print(df.info())
    print(df.describe())
    print(df.columns)    