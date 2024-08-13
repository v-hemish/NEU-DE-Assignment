from flask import Flask, jsonify, request
from query_twitter_data import (
    count_tweets_by_term_per_day,
    count_unique_users_by_term,
    average_likes_by_term,
    get_place_ids_by_term,
    tweet_times_by_term,
    most_active_user_by_term,
    top_hashtags_by_term,
    top_sources_by_term,
    most_liked_tweet_by_term,
    retweet_count_distribution,
    tweets
)
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/tweets_by_term_per_day', methods=['GET'])
def get_tweets_by_term_per_day():
    term = request.args.get('term')
    result = count_tweets_by_term_per_day(tweets, term)
    return jsonify(result)

@app.route('/unique_users_by_term', methods=['GET'])
def get_unique_users_by_term():
    term = request.args.get('term')
    result = count_unique_users_by_term(tweets, term)
    return jsonify({"unique_users": result})

@app.route('/average_likes_by_term', methods=['GET'])
def get_average_likes_by_term():
    term = request.args.get('term')
    result = average_likes_by_term(tweets, term)
    return jsonify({"average_likes": result})

@app.route('/place_ids_by_term', methods=['GET'])
def get_place_ids_by_term():
    term = request.args.get('term')
    result = get_place_ids_by_term(tweets, term)
    return jsonify(result)

@app.route('/tweet_times_by_term', methods=['GET'])
def get_tweet_times_by_term():
    term = request.args.get('term')
    result = tweet_times_by_term(tweets, term)
    return jsonify(result)

@app.route('/most_active_user_by_term', methods=['GET'])
def get_most_active_user_by_term():
    term = request.args.get('term')
    result = most_active_user_by_term(tweets, term)
    return jsonify(result)

@app.route('/top_hashtags_by_term', methods=['GET'])
def get_top_hashtags_by_term():
    term = request.args.get('term')
    limit = int(request.args.get('limit', 5))
    result = top_hashtags_by_term(tweets, term, limit)
    return jsonify(result)

@app.route('/top_sources_by_term', methods=['GET'])
def get_top_sources_by_term():
    term = request.args.get('term')
    limit = int(request.args.get('limit', 5))
    result = top_sources_by_term(tweets, term, limit)
    return jsonify(result)

@app.route('/most_liked_tweet_by_term', methods=['GET'])
def get_most_liked_tweet_by_term():
    term = request.args.get('term')
    result = most_liked_tweet_by_term(tweets, term)
    return jsonify(result)

@app.route('/retweet_count_distribution', methods=['GET'])
def get_retweet_count_distribution():
    term = request.args.get('term')
    result = retweet_count_distribution(tweets, term)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
