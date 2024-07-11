import app_functions.data_manipulation as dm
import app_functions.requests as req

def write_bookmakers_to_txt(bookmakers, error=False):
    # write bookmakers to bookmakers.txt
    with open("bookies.txt", "w") as f:
        for bookmaker in bookmakers:
            f.write(bookmaker + "\n")
    
    if error:
        print(f"Error occurred, incomplete bookmakers list written to bookies.txt")    
    else:
        print(f"Bookmakers list written to bookies.txt")

if __name__ == "__main__":
    api_token = dm.read_config(build=True)

    sports = req.get_sports_request(api_token)

    # try to read sports.txt
    try:
        with open("sports.txt", "r") as f:
            old_sports = set(f.read().splitlines())
    except FileNotFoundError:
        old_sports = set()

    # combine old and new sports
    sports = old_sports.union(sports)

    # write sports to sports.txt
    with open("sports.txt", "w") as f:
        for sport in sports:
            f.write(sport + "\n")
    
    print("Sports written to sports.txt")

    # list of current regions
    regions = ["eu", "us", "uk", "au", "us2"]

    # get bookmakers
    bookmakers = set()
    for sport in sports:
        for region in regions:
            try:
                new_bookmakers = req.get_bookmakers_request(api_token, sport, region)
                # combine old and new bookmakers
                bookmakers = bookmakers.union(new_bookmakers)
            except Exception as e:
                print(f"Error: {e}, quitting...")
                write_bookmakers_to_txt(bookmakers, error=True)
                exit()
    
    write_bookmakers_to_txt(bookmakers)
