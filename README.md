
# Twitter Data Processing and Analysis Project

## Overview

This project consists of a series of Python scripts designed to preprocess Twitter data, load it into MongoDB, and perform various analyses on the data. The project is structured into five main components, each with specific functionality:

1. **Data Preprocessing**: Clean and prepare raw Twitter data stored in TSV files.
2. **Data Loading**: Load the cleaned data into a MongoDB database.
3. **Data Querying**: Perform various analyses on the Twitter data stored in MongoDB.
4. **Flask API**: Provide a RESTful API to query the data using Flask.
5. **Unit Testing**: Ensure the correctness of data processing and analysis functions using unit tests.

## File Descriptions

### 1. `clean_and_save_tsv.py`
This script preprocesses large Twitter datasets stored in TSV format, making them ready for further analysis. It handles tasks such as timestamp conversion, list conversion, text normalization, and filling missing values.

**Key Features**:
- Processes data in chunks for efficient memory usage.
- Converts stringified lists and timestamps to appropriate formats.
- Handles missing values and normalizes text data.

**Usage**:
```bash
python clean_and_save_tsv.py
```

### 2. `load_to_mongodb.py`
This script loads the cleaned Twitter data from the TSV file into a MongoDB collection.

**Key Features**:
- Loads data in chunks for efficient processing.
- Connects to a local MongoDB instance and inserts records into a specified collection.

**Usage**:
```bash
python load_to_mongodb.py
```

### 3. `query_twitter_data.py`
This script provides various functions to query the Twitter data stored in MongoDB. It includes operations like counting tweets by day, finding the most active users, and identifying popular hashtags.

**Key Features**:
- Supports complex aggregation queries to analyze Twitter data.
- Functions can be executed directly or integrated into a Flask API for broader use.

**Usage**:
```bash
python query_twitter_data.py
```

### 4. `app.py` - Flask API
This script provides a RESTful API using Flask to query the Twitter data stored in MongoDB. It includes various endpoints to retrieve data such as the number of tweets per day, unique users, average likes, and more.

**Key Features**:
- RESTful API for querying MongoDB data.
- Includes CORS support for cross-origin requests.

**Example Endpoints**:

- **Tweets by term per day**:
  ```
  GET /tweets_by_term_per_day?term=music
  ```
  Returns the count of tweets containing the term "music" per day.

- **Unique users by term**:
  ```
  GET /unique_users_by_term?term=music
  ```
  Returns the number of unique users who posted tweets containing the term "music".

- **Average likes by term**:
  ```
  GET /average_likes_by_term?term=music
  ```
  Returns the average number of likes for tweets containing the term "music".

- **Place IDs by term**:
  ```
  GET /place_ids_by_term?term=music
  ```
  Returns the place IDs where tweets containing the term "music" were posted.

- **Most liked tweet by term**:
  ```
  GET /most_liked_tweet_by_term?term=music
  ```
  Returns the most liked tweet containing the term "music".

**Usage**:
```bash
python app.py
```

**Testing**: Use Postman or a web browser to interact with the API.

### 5. `test.py`
This script contains unit tests for the query functions in `query_twitter_data.py`. The tests use `pytest` and `unittest.mock` to simulate database operations and validate the logic of each function.

**Key Features**:
- Ensures correctness and reliability of query functions.
- Uses mock objects to simulate MongoDB interactions.

**Usage**:
```bash
pytest test.py
```

## Requirements

- `pandas`
- `pymongo`
- `flask`
- `flask-cors`
- `pytest`

**Install dependencies**:
```bash
pip install -r requirements.txt
```

## Summary

This project provides a robust framework for processing, storing, and analyzing Twitter data. By breaking down the tasks into preprocessing, loading, querying, and testing, the project ensures that the data is clean, efficiently stored, and correctly analyzed.
