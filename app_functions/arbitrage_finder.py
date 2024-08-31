import pandas as pd
import itertools

def build_bookie_pairs_df_from_request(df):
    new_df = pd.DataFrame(columns=['sport','game_id', 'bookie1', 'bookie2'])

    for game_id, group in df.groupby('game_id'):
        sport = group['sport'].iloc[0]
        bookies = group['bookmaker'].unique()
        for bookie1, bookie2 in itertools.combinations(bookies, 2):
            new_index = len(new_df)
            new_row = {'game_id': game_id, 'bookie1': bookie1, 'bookie2': bookie2, 'sport': sport}
            new_df.loc[new_index] = new_row

    new_df.drop_duplicates(inplace=True)
    new_df.dropna(inplace=True)
    new_df.reset_index(drop=True, inplace=True)

    return new_df

def get_bookie_team(df, row, bookie_num, type):
    # Build the column name dynamically based on bookie number and type
    odds_column = "favorite" if type == "favorite" else "underdog"
    
    filtered_df = df[(df["bookmaker"] == row[bookie_num]) & (df["game_id"] == row["game_id"])]

    # Assuming there's only one matching row, get the specified odds value
    if not filtered_df.empty:
        return filtered_df[odds_column].iloc[0]
    else:
        return None  # or some default value
    
def get_odds(df, row, bookie_num, type):
    odds_column = "odds favorite" if type == "favorite" else "odds underdog"
    
    # Filter df for the current row's bookie and game_id
    filtered_df = df[(df["bookmaker"] == row[bookie_num]) & (df["game_id"] == row["game_id"])]
    
    # Assuming there's only one matching row, get the specified odds value
    if not filtered_df.empty:
        return filtered_df[odds_column].iloc[0]
    else:
        return None  # or some default value
    
def fav_bet_winnings(bet_amount, odds):
    return ((bet_amount * 100 / -(odds)) + bet_amount)

def dog_bet_winnings(bet_amount, odds):
    return ((bet_amount * odds / 100) + bet_amount)

def bet_winnings(bet_amount, odds):
    if odds > 100:
        return fav_bet_winnings(bet_amount, odds)
    else:
        return dog_bet_winnings(bet_amount, odds)

def arb_available(dog_odds, dog_bet, fav_odds, fav_bet):
    if((bet_winnings(dog_bet, dog_odds) > dog_bet + fav_bet) and (bet_winnings(fav_bet, fav_odds) > dog_bet + fav_bet)):
        return True
        
    return False

def set_arb(row):
    dog_odds = row["max_underdog_odds"]
    fav_odds = row["max_favorite_odds"]

    if (fav_odds > 100 and dog_odds > 100):
        row["arb_available"] = True
        row["favorite_bet_amount"] = 50
        row["underdog_bet_amount"] = 50
        row["arb_min_profit"] = 0

    min_distance = 100000
    optimal_i = 0
    # cant lose more than the full combined bet
    min_profit = -100
    can_arb = False

    for i in range(1, 99):
        fav_bet = i
        dog_bet = 100 - i

        dog_winnings = dog_bet_winnings(dog_bet, dog_odds)
        fav_winnings = fav_bet_winnings(fav_bet, fav_odds)

        profit = min(dog_winnings, fav_winnings) - 100

        if(arb_available(dog_odds, dog_bet, fav_odds, fav_bet)):
            can_arb = True

        diff = abs(dog_winnings - fav_winnings)
        if diff < min_distance:
            min_distance = diff
            optimal_i = i
            min_profit = profit
    
    row["arb_available"] = can_arb
    row["favorite_bet_amount"] = optimal_i
    row["underdog_bet_amount"] = 100 - optimal_i
    row["arb_min_profit"] = min_profit

    return row

def build_odds_df(bookie_pairs_df):
    bookie_pairs_df["bookie1_favorite_odds"] = bookie_pairs_df.apply(lambda row : get_odds(row, bookie_num='bookie1', type='favorite'), axis=1)
    bookie_pairs_df["bookie1_favorite"] = bookie_pairs_df.apply(lambda row: get_bookie_team(row, bookie_num = 'bookie1', type='favorite'), axis=1)
    bookie_pairs_df["bookie2_favorite_odds"] = bookie_pairs_df.apply(lambda row: get_odds(row, bookie_num='bookie2', type='favorite'), axis=1)
    bookie_pairs_df["bookie2_favorite"] = bookie_pairs_df.apply(lambda row: get_bookie_team(row, bookie_num = 'bookie2', type='favorite'), axis=1)
    bookie_pairs_df["bookie1_underdog_odds"] = bookie_pairs_df.apply(lambda row: get_odds(row, bookie_num='bookie1', type='underdog'), axis=1)
    bookie_pairs_df["bookie1_underdog"] = bookie_pairs_df.apply(lambda row: get_bookie_team(row, bookie_num = 'bookie1', type='underdog'), axis=1)
    bookie_pairs_df["bookie2_underdog_odds"] = bookie_pairs_df.apply(lambda row: get_odds(row, bookie_num='bookie2', type='underdog'), axis=1)
    bookie_pairs_df["bookie2_underdog"] = bookie_pairs_df.apply(lambda row: get_bookie_team(row, bookie_num = 'bookie2', type='underdog'), axis=1)

    return bookie_pairs_df

def build_diff_df(new_df):
    new_df["max_favorite_odds"] = new_df[["bookie1_favorite_odds", "bookie2_favorite_odds"]].max(axis=1)
    new_df["max_underdog_odds"] = new_df[["bookie1_underdog_odds", "bookie2_underdog_odds"]].max(axis=1)
    new_df["favorite_diff"] = (new_df["bookie1_favorite_odds"] - new_df["bookie2_favorite_odds"]).abs()

    # create new df with only the rows with the max difference in odds for each game_id
    diff_df = new_df.loc[new_df.groupby('game_id')['favorite_diff'].idxmax()]
    diff_df.dropna(inplace=True)
    diff_df.reset_index(drop=True, inplace=True)

    diff_df["favorite_bookie"] = diff_df.apply(lambda row: row["bookie1"] if row["bookie1_favorite_odds"] > row["bookie2_favorite_odds"] else row["bookie2"], axis=1)
    diff_df["underdog_bookie"] = diff_df.apply(lambda row: row["bookie1"] if row["bookie1_underdog_odds"] > row["bookie2_underdog_odds"] else row["bookie2"], axis=1)

    diff_df["favorite_bookie_team"] = diff_df.apply(lambda row: row["bookie1_favorite"] if row["bookie1_favorite_odds"] > row["bookie2_favorite_odds"] else row["bookie2_favorite"], axis=1)
    diff_df["underdog_bookie_team"] = diff_df.apply(lambda row: row["bookie1_underdog"] if row["bookie1_underdog_odds"] > row["bookie2_underdog_odds"] else row["bookie2_underdog"], axis=1)

    return diff_df

def build_arb_df(diff_df):
    needed_cols = ["sport","game_id", "favorite_bookie", "favorite_bookie_team", "max_favorite_odds", "underdog_bookie", "underdog_bookie_team", "max_underdog_odds"]
    arbitrage_df = diff_df[needed_cols]
    arbitrage_df["arb_available"] = False

    for index, row in diff_df.iterrows():
        if (row["bookie1_favorite"] != row["bookie2_favorite"] and (row["bookie1_favorite_odds"] > 100) and (row["bookie2_favorite_odds"] > 100)):
            print(row)
    
    arbitrage_df = arbitrage_df.apply(set_arb, axis=1)

def get_valid_arbs(arbitrage_df):
    return arbitrage_df[arbitrage_df["arb_available"] == True]

def build_full_arbitrage_df(request_as_df):
    bookie_pairs_df = build_bookie_pairs_df_from_request(request_as_df)
    full_odds_df = build_odds_df(bookie_pairs_df)
    diff_df = build_diff_df(full_odds_df)
    arb_df = build_arb_df(diff_df)
    valid_arbs = get_valid_arbs(arb_df)
    
    return valid_arbs

def display_arbs(all_valid_arbs):
    # loop through all valid arbs and display them
    for index, row in all_valid_arbs.iterrows():
        print("Sport: " + row["sport"] + " Game ID: " + row["game_id"])
        print("\tBet " + str(row["favorite_bet_amount"]) + " on " + row["favorite_bookie_team"] + " at " + str(row["max_favorite_odds"]) + " on " + row["favorite_bookie"])
        print("\tBet " + str(row["underdog_bet_amount"]) + " on " + row["underdog_bookie_team"] + " at " + str(row["max_underdog_odds"]) + " on " + row["underdog_bookie"])
        
        print("\tArbitrage Attempt Minimum Profit: $" + str(row["arb_min_profit"]))
        print("\n")