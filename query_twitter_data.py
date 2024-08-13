from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.twitter_db
tweets = db.tweets

# 1. How many tweets were posted containing the term on each day?
def count_tweets_by_term_per_day(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$addFields': {'created_at': {'$toDate': '$created_at'}}},  # Convert string to date
        {'$group': {
            '_id': {'$dateToString': {'format': "%Y-%m-%d", 'date': "$created_at"}},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]
    return list(collection.aggregate(pipeline))

# 2. How many unique users posted a tweet containing the term?
def count_unique_users_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': "$author_id"}},
        {'$count': "unique_users"}
    ]
    result = collection.aggregate(pipeline)
    return next(result, {"unique_users": 0})['unique_users']

# 3. How many likes did tweets containing the term get, on average?
def average_likes_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': None, 'average_likes': {'$avg': "$like_count"}}}
    ]
    result = collection.aggregate(pipeline)
    return next(result, {"average_likes": 0})['average_likes']

# 4. Where (in terms of place IDs) did the tweets come from?
def get_place_ids_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': "$place_id", 'count': {'$sum': 1}}}
    ]
    return list(collection.aggregate(pipeline))

# 5. What times of day were the tweets posted at?
def tweet_times_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$addFields': {'created_at': {'$toDate': '$created_at'}}},  # Convert string to date
        {'$group': {
            '_id': {'$hour': "$created_at"},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}}
    ]
    return list(collection.aggregate(pipeline))

# 6. Which user posted the most tweets containing the term?
def most_active_user_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': "$author_id", 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 1}
    ]
    result = collection.aggregate(pipeline)
    return next(result, None)

# 7. Top 5 hashtags associated with the term
def top_hashtags_by_term(collection, term, limit=5):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}, 'hashtags': {'$ne': []}}},  # Exclude empty hashtags
        {'$unwind': '$hashtags'},
        {'$group': {'_id': "$hashtags", 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': limit}
    ]
    return list(collection.aggregate(pipeline))

# 8. Top 5 sources of tweets containing the term
def top_sources_by_term(collection, term, limit=5):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': "$source", 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': limit}
    ]
    return list(collection.aggregate(pipeline))

# 9. Most liked tweet containing the term
def most_liked_tweet_by_term(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$sort': {'like_count': -1}},
        {'$limit': 1},
        {'$project': {'_id': 0, 'id': 1, 'text': 1, 'like_count': 1}}
    ]
    return list(collection.aggregate(pipeline))

# 10. Retweet count distribution for tweets containing the term
def retweet_count_distribution(collection, term):
    pipeline = [
        {'$match': {'text': {'$regex': term, '$options': 'i'}}},
        {'$group': {'_id': "$retweet_count", 'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ]
    return list(collection.aggregate(pipeline))

# Main function to run all queries
def main():
    term = input("Enter the term to search for: ")

    print("\n########## Query Results ##########")

    # 1. Tweets by day
    print("\n----- Number of tweets containing the term '{}' per day -----".format(term))
    tweets_per_day = count_tweets_by_term_per_day(tweets, term)
    for day in tweets_per_day:
        print(f"Date: {day['_id']}, Count: {day['count']}")

    # 2. Unique users
    print("\n----- Number of unique users who posted tweets containing the term '{}' -----".format(term))
    unique_users = count_unique_users_by_term(tweets, term)
    print(f"Unique Users: {unique_users}")

    # 3. Average likes
    print("\n----- Average number of likes for tweets containing the term '{}' -----".format(term))
    avg_likes = average_likes_by_term(tweets, term)
    print(f"Average Likes: {avg_likes}")

    # 4. Place IDs
    print("\n----- Places (by place_id) where tweets containing the term '{}' were posted -----".format(term))
    place_ids = get_place_ids_by_term(tweets, term)
    for place in place_ids:
        print(f"Place ID: {place['_id']}, Count: {place['count']}")

    # 5. Times of day
    print("\n----- Times of day when tweets containing the term '{}' were posted -----".format(term))
    times_of_day = tweet_times_by_term(tweets, term)
    for time in times_of_day:
        print(f"Hour: {time['_id']}, Count: {time['count']}")

    # 6. Most active user
    print("\n----- User who posted the most tweets containing the term '{}' -----".format(term))
    most_active_user = most_active_user_by_term(tweets, term)
    if most_active_user:
        print(f"User ID: {most_active_user['_id']}, Tweet Count: {most_active_user['count']}")
    else:
        print(f"No tweets containing the term '{term}' found.")

    # 7. Top hashtags
    print("\n----- Top 5 hashtags in tweets containing the term '{}' -----".format(term))
    top_hashtags = top_hashtags_by_term(tweets, term)
    for hashtag in top_hashtags:
        print(f"Hashtag: {hashtag['_id']}, Count: {hashtag['count']}")

    # 8. Top sources
    print("\n----- Top 5 sources for tweets containing the term '{}' -----".format(term))
    top_sources = top_sources_by_term(tweets, term)
    for source in top_sources:
        print(f"Source: {source['_id']}, Count: {source['count']}")

    # 9. Most liked tweet
    print("\n----- Most liked tweet containing the term '{}' -----".format(term))
    most_liked_tweet = most_liked_tweet_by_term(tweets, term)
    if most_liked_tweet:
        for tweet in most_liked_tweet:
            print(f"Tweet ID: {tweet['id']}, Likes: {tweet['like_count']}\nText: {tweet['text']}")
    else:
        print(f"No tweets containing the term '{term}' found.")

    # 10. Retweet count distribution
    print("\n----- Retweet count distribution for tweets containing the term '{}' -----".format(term))
    retweet_distribution = retweet_count_distribution(tweets, term)
    for retweet in retweet_distribution:
        print(f"Retweet Count: {retweet['_id']}, Number of Tweets: {retweet['count']}")

    print("\n###################################")

if __name__ == '__main__':
    main()
