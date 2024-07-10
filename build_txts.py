import app_functions.data_manipulation as dm
import app_functions.requests as req

if __name__ == "__main__":
    api_token = dm.read_config(build=True)

    sports = req.get_sports_request(api_token)

    # Write sports to file
    with open("sports.txt", "w") as f:
        for sport in sports:
            f.write(f"{sport}\n")
    
    print("Sports written to sports.txt")