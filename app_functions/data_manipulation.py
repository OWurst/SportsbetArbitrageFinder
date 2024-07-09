import yaml

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
    