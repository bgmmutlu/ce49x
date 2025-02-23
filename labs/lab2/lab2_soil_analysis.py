import pandas as pd

# Loading data from a CSV file with error handling
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: The file is not formatted correctly.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return None

# Cleaning the data with error handling
def clean_data(data):
    try:
        if data is None:
            raise ValueError("No data available to clean.")

        # Filling missing values with the column mean
        data = data.fillna(data.mean())

        # Reseting index after cleaning, ensuring index is sequential after cleaning
        data = data.reset_index(drop=True)
        return data
    except ValueError as e:
        print(f"Data Cleaning Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data cleaning: {e}")
        return None

# Function to compute statistics for each column excluding 'sample_id' with error handling
def compute_statistics(data):
    try:
        if data is None:
            raise ValueError("No data available to compute statistics.")

        # Droping 'sample_id' column if it exists
        data_without_sample_id = data.drop(columns=['sample_id'], errors='ignore')

        statistics = {}

        # Calculating the desired statistics for each column
        for column in data_without_sample_id.columns:
            column_data = data_without_sample_id[column]

            statistics[column] = {
                "minimum": column_data.min(),
                "maximum": column_data.max(),
                "mean": column_data.mean(),
                "median": column_data.median(),
                "std_dev": column_data.std()
            }

        return statistics
    except ValueError as e:
        print(f"Statistics Computation Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while computing statistics: {e}")
        return None

# Loading the dataset
file_path = '/Users/begummutlu/CE49X-Spring25/datasets/soil_test.csv'
data = load_data(file_path)

# Checking if the data was loaded successfully
if data is not None:
    # Cleaning the loaded data
    cleaned_data = clean_data(data)

    # Checking if the data was cleaned successfully
    if cleaned_data is not None:
        # Computing statistics for all columns excluding 'sample_id'
        statistics = compute_statistics(cleaned_data)

        # Checking if statistics were computed successfully
        if statistics is not None:
            # Print the statistics in the desired format
            print("Statistics:")
            for column, stat_values in statistics.items():
                print(f"sample_type: {column}")
                for stat, value in stat_values.items():
                    print(f"{stat.capitalize()}: {value}")
                print("-" * 40)  # Adds a line separator between columns
        else:
            print("Failed to compute statistics.")
    else:
        print("Failed to clean data.")
else:
    print("Failed to load data.")


    

