import pandas as pd
import ast
import csv

def preprocess_data(df):
    """
    Preprocess the data to ensure it is ready for querying.
    :param df: DataFrame containing the data
    :return: Cleaned DataFrame
    """
    # Convert timestamps to datetime objects with UTC
    df['ts1'] = pd.to_datetime(df['ts1'], errors='coerce', utc=True)
    df[' ts2'] = pd.to_datetime(df[' ts2'], errors='coerce', utc=True)
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)

    # Convert stringified lists to actual lists (e.g., hashtags)
    if 'hashtags' in df.columns:
        df['hashtags'] = df['hashtags'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    # Clean text data (optional, can be extended)
    df['text'] = df['text'].apply(lambda x: x.lower() if pd.notnull(x) else x)

    # Fill missing values for specific columns that are safe to fill with scalar values
    scalar_fill_values = {
        'replied_to_follower_count': 0,
        'quoted_follower_count': 0,
        'retweeted_follower_count': 0,
    }
    df.fillna(scalar_fill_values, inplace=True)

    # Handle columns that require filling with lists or None separately
    list_fill_columns = ['hashtags', 'mentioned_author_ids', 'mentioned_handles']
    for col in list_fill_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])

    # Handle filling with None for appropriate columns
    none_fill_columns = [
        'replied_to', 'replied_to_author_id', 'replied_to_handle',
        'quoted', 'quoted_author_id', 'quoted_handle',
        'retweeted', 'retweeted_author_id', 'retweeted_handle',
        'urls', 'media_keys', 'place_id'
    ]
    for col in none_fill_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

    return df

def load_and_process_tsv(file_path, output_file, chunksize=100000):
    """
    Load the data in chunks, preprocess it, and write to a new TSV file.
    :param file_path: Path to the original TSV file
    :param output_file: Path to the output cleaned TSV file
    :param chunksize: Number of rows per chunk to load
    """
    try:
        with pd.read_csv(file_path, sep='\t', chunksize=chunksize, engine='python', quoting=csv.QUOTE_NONE, on_bad_lines='warn') as reader:
            for i, chunk in enumerate(reader):
                cleaned_chunk = preprocess_data(chunk)
                if i == 0:
                    cleaned_chunk.to_csv(output_file, sep='\t', index=False, mode='w')
                else:
                    cleaned_chunk.to_csv(output_file, sep='\t', index=False, mode='a', header=False)
    except pd.errors.ParserError as e:
        print(f"Error parsing the file: {e}")
        raise

def main():
    # Define the path to your original TSV file (replace with the actual file path)
    file_path = 'correct_twitter_202102.tsv'
    
    # Define the path to the output cleaned TSV file
    output_file = 'cleaned_twitter_202102.tsv'

    # Load, clean, and save the data
    load_and_process_tsv(file_path, output_file)

if __name__ == '__main__':
    main()
