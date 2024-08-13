import pandas as pd

def load_sample(file_path, nrows=5):
    """
    Load a small sample of the data to inspect.
    :param file_path: Path to the TSV file
    :param nrows: Number of rows to load (default is 5)
    :return: DataFrame containing the sample data
    """
    return pd.read_csv(file_path, sep='\t', nrows=nrows)

def inspect_data(df):
    """
    Print out information to understand the data structure and content.
    :param df: DataFrame containing the data
    """
    print("First few rows of the data:\n")
    print(df.head())
    print("\nDataFrame Info:\n")
    print(df.info())
    print("\nSummary of the Data:\n")
    print(df.describe(include='all'))
    print("\nMissing values in each column:\n")
    print(df.isnull().sum())

def main():
    # Define the path to your TSV file (replace with the actual file path)
    file_path = 'correct_twitter_202102.tsv'

    # Load a small sample of the data
    sample_df = load_sample(file_path)

    # Inspect the data
    inspect_data(sample_df)

if __name__ == '__main__':
    main()
