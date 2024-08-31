import pandas as pd
import app_functions.data_manipulation as dm
import app_functions.requests as req
import app_functions.arbitrage_finder as af

if __name__ == "__main__":
    config = dm.read_config()

    # read sport as sport field in config
    sports = config["sports"]
    token = config["api_token"]
    bookmakers = config["bookmakers"]

    # get odds for each sport COMMENT OUT FOR TESTING
    all_odds = [] 
    for sport in sports:
        # comment this out for testing #odds = req.get_odds_request(token, sport, bookmakers)

        odds = req.get_test_odds_request(f"{sport}_odds.json")
        # save odds as json
        # comment this out for testing# dm.save_json(odds, f"{sport}_odds.json")
        all_odds.append(odds)

    #all_odds = req.get_test_odds_request()

    # ## for testing save as json
    # save list of odds as json
    
    # convert to dataframe
    df = dm.json_to_df(all_odds)
    arb_df = af.build_full_arbitrage_df(df)

    if arb_df.empty:
        print("No arbitrage opportunities found.")
    else:
        af.display_arbs(arb_df)
        # save arbitrage opportunities as json
        dm.save_json(arb_df, "arbitrage_opportunities.json")