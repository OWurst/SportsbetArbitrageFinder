import pandas as pd
import app_functions.data_manipulation as dm

if __name__ == "__main__":
    config = dm.read_config()
    
    print(config)