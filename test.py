import pytest
from unittest.mock import MagicMock
from query_twitter_data import (
    count_tweets_by_term_per_day,
    count_unique_users_by_term,
    average_likes_by_term,
    most_active_user_by_term,
    top_hashtags_by_term,
    most_liked_tweet_by_term
)

@pytest.fixture
def mock_collection():
    return MagicMock()

def test_count_tweets_by_term_per_day(mock_collection):
    term = 'music'
    mock_collection.aggregate.return_value = iter([
        {"_id": "2021-01-01", "count": 10},
        {"_id": "2021-01-02", "count": 20},
        {"_id": "2021-01-03", "count": 30}
    ])
    result = count_tweets_by_term_per_day(mock_collection, term)
    mock_collection.aggregate.assert_called_once()
    assert len(result) == 3  # Expected 3 entries for 3 days
    assert result[0]['_id'] == "2021-01-01"
    assert result[1]['count'] == 20

def test_count_tweets_by_term_per_day_no_results(mock_collection):
    term = 'music'
    mock_collection.aggregate.return_value = iter([])
    result = count_tweets_by_term_per_day(mock_collection, term)
    assert len(result) == 0  # Expected no entries

def test_count_unique_users_by_term(mock_collection):
    mock_collection.aggregate.return_value = iter([{"unique_users": 10}])
    term = 'music'
    result = count_unique_users_by_term(mock_collection, term)
    assert result == 10

def test_count_unique_users_by_term_no_results(mock_collection):
    mock_collection.aggregate.return_value = iter([])
    term = 'music'
    result = count_unique_users_by_term(mock_collection, term)
    assert result == 0  # Expected 0 unique users

def test_average_likes_by_term(mock_collection):
    mock_collection.aggregate.return_value = iter([{"average_likes": 15}])
    term = 'music'
    result = average_likes_by_term(mock_collection, term)
    assert result == 15

def test_average_likes_by_term_no_results(mock_collection):
    mock_collection.aggregate.return_value = iter([])
    term = 'music'
    result = average_likes_by_term(mock_collection, term)
    assert result == 0  # Expected 0 average likes

def test_most_active_user_by_term(mock_collection):
    mock_collection.aggregate.return_value = iter([{"_id": "user1", "count": 10}])
    term = 'music'
    result = most_active_user_by_term(mock_collection, term)
    assert result['_id'] == "user1"
    assert result['count'] == 10

def test_most_active_user_by_term_no_results(mock_collection):
    mock_collection.aggregate.return_value = iter([])
    term = 'music'
    result = most_active_user_by_term(mock_collection, term)
    assert result is None  # Expected no active user

def test_top_hashtags_by_term(mock_collection):
    mock_collection.aggregate.return_value = iter([
        {"_id": "music", "count": 50},
        {"_id": "pop", "count": 40},
        {"_id": "rock", "count": 30}
    ])
    term = 'music'
    result = top_hashtags_by_term(mock_collection, term)
    assert len(result) == 3  # Expected 3 hashtags
    assert result[0]['_id'] == 'music'
    assert result[1]['count'] == 40

def test_top_hashtags_by_term_no_results(mock_collection):
    mock_collection.aggregate.return_value = iter([])
    term = 'music'
    result = top_hashtags_by_term(mock_collection, term)
    assert len(result) == 0  # Expected no hashtags

def test_most_liked_tweet_by_term(mock_collection):
    mock_collection.aggregate.return_value = iter([{"id": "tweet1", "like_count": 15}])
    term = 'music'
    result = most_liked_tweet_by_term(mock_collection, term)
    assert result[0]['like_count'] == 15  # Assuming the most liked tweet has 15 likes

def test_most_liked_tweet_by_term_no_results(mock_collection):
    mock_collection.aggregate.return_value = iter([])
    term = 'music'
    result = most_liked_tweet_by_term(mock_collection, term)
    assert len(result) == 0  # Expected no liked tweets
