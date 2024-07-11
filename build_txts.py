import app_functions.data_manipulation as dm
import app_functions.requests as req

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

    # get list of regions
    regions = input("Enter regions separated by commas: ")
    regions = [region.strip() for region in regions.split(",")]

    # get bookmakers
    for sport in sports:
        bookmakers = req.get_bookmakers_request(api_token, sport, regions)

        # try to read bookies.txt
        try:
            with open("bookies.txt", "r") as f:
                old_bookmakers = set(f.read().splitlines())
        except FileNotFoundError:
            old_bookmakers = set()

        # combine old and new bookmakers
        bookmakers = old_bookmakers.union(bookmakers)

        # write bookmakers to bookmakers.txt
        with open("bookies.txt", "w") as f:
            for bookmaker in bookmakers:
                f.write(bookmaker + "\n")
        
        print(f"Bookmakers for {sport} written to bookies.txt")