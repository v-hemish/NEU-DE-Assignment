import pandas as pd
from pymongo import MongoClient
import json

def load_data_to_mongodb(file_path, db_name, collection_name, chunk_size=10000):
    """
    Load cleaned data from a TSV file into a MongoDB collection.
    :param file_path: Path to the cleaned TSV file
    :param db_name: Name of the MongoDB database
    :param collection_name: Name of the MongoDB collection
    :param chunk_size: Number of rows to process at a time
    """
    client = MongoClient('localhost', 27017)  # Connect to MongoDB server
    db = client[db_name]  # Access the database
    collection = db[collection_name]  # Access the collection
    
    # Process the data in chunks
    for chunk in pd.read_csv(file_path, sep='\t', chunksize=chunk_size):
        # Convert DataFrame to dictionary and insert into MongoDB
        records = json.loads(chunk.to_json(orient='records'))
        collection.insert_many(records)
        print(f'Inserted {len(records)} records into MongoDB.')

    print(f'Data loaded successfully into {db_name}.{collection_name}.')

def main():
    # Define the path to your cleaned TSV file
    file_path = 'cleaned_twitter_202102.tsv'
    
    # Define the MongoDB database and collection names
    db_name = 'twitter_db'
    collection_name = 'tweets'

    # Load the data into MongoDB
    load_data_to_mongodb(file_path, db_name, collection_name)

if __name__ == '__main__':
    main()
