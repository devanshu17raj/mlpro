import pandas as pd

# This is the path to your raw data file
data_path = r'G:\MLproject\src\notebook\data\stud.CSV'

# Read the CSV into a DataFrame
try:
    df = pd.read_csv(data_path)
    # Print all column names as a list
    print("Here are the column names in your CSV file:")
    print(df.columns.tolist())
except FileNotFoundError:
    print(f"Error: The file was not found at '{data_path}'")
except Exception as e:
    print(f"An error occurred: {e}")
    