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
    
def build_odds_df(bookie_pairs_df):
    bookie_pairs_df["bookie1_favorite_odds"] = bookie_pairs_df.apply(get_odds, bookie_num='bookie1', type='favorite', axis=1)
    bookie_pairs_df["bookie1_favorite"] = bookie_pairs_df.apply(get_bookie_team, bookie_num = 'bookie1', type='favorite', axis=1)
    bookie_pairs_df["bookie2_favorite_odds"] = bookie_pairs_df.apply(get_odds, bookie_num='bookie2', type='favorite', axis=1)
    bookie_pairs_df["bookie2_favorite"] = bookie_pairs_df.apply(get_bookie_team, bookie_num = 'bookie2', type='favorite', axis=1)
    bookie_pairs_df["bookie1_underdog_odds"] = bookie_pairs_df.apply(get_odds, bookie_num='bookie1', type='underdog', axis=1)
    bookie_pairs_df["bookie1_underdog"] = bookie_pairs_df.apply(get_bookie_team, bookie_num = 'bookie1', type='underdog', axis=1)
    bookie_pairs_df["bookie2_underdog_odds"] = bookie_pairs_df.apply(get_odds, bookie_num='bookie2', type='underdog', axis=1)
    bookie_pairs_df["bookie2_underdog"] = bookie_pairs_df.apply(get_bookie_team, bookie_num = 'bookie2', type='underdog', axis=1)

    return bookie_pairs_df

def build_full_arbitrage_df(request_as_df):
    bookie_pairs_df = build_bookie_pairs_df_from_request(request_as_df)
    full_arbitrage_df = build_odds_df(bookie_pairs_df)
    
    
    
    return full_arbitrage_df