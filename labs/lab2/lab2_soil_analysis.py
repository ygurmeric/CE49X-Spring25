import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load the dataset using Pandas.
    Handles the case when the file is not found.
    """
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

def clean_data(df):
    """
    Clean the dataset by handling missing values and optionally removing outliers.
    """
    if df is None:
        return None

    # Fill missing values with column mean
    df.fillna(df.mean(), inplace=True)
    print("Missing values handled.")

    # Optional: Remove outliers for soil_ph
    if 'soil_ph' in df.columns:
        mean_ph = df['soil_ph'].mean()
        std_ph = df['soil_ph'].std()
        df = df[np.abs(df['soil_ph'] - mean_ph) <= (3 * std_ph)]
        print("Outliers removed from soil_ph column.")

    return df

def compute_statistics(df, column):
    """
    Compute and print descriptive statistics for the given numeric column.
    """
    if df is None or column not in df.columns:
        print(f"Error: Column '{column}' not found in the dataset.")
        return

    stats = {
        "Minimum": df[column].min(),
        "Maximum": df[column].max(),
        "Mean": df[column].mean(),
        "Median": df[column].median(),
        "Standard Deviation": df[column].std()
    }

    print("\nDescriptive Statistics for", column)
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")

def main():
    """
    Main function to run the analysis.
    """
    file_path = "../../datasets/soil_test.csv"
    df = load_data(file_path)
    df = clean_data(df)

    if df is not None:
        compute_statistics(df, "soil_ph")

if __name__ == "__main__":
    main()