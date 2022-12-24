import time
import pandas as pd
import tweepy as tw


def create_user_db(bearer_token, tweet_data):
    """
    Creates and saves a database of the users included in tweet data
    :param bearer_token: Bearer token to access Twitter API
    :param tweet_data: A dataframe containing tweet data including user IDs
    :return: void, but saves a csv file of the resulting user database
    """

    # Set up twitter api
    client = tw.Client(bearer_token)

    # Create list of use IDs from tweet database
    users = tweet_data[tweet_data['author_id'] != '']
    users = list(set(users['author_id'].tolist()))
    users = list(filter(None, users))
    users = list(map(int, users))
    print("Total number of distinct users found:" + str(len(users)))

    # Generate user db
    df_user_db = pd.DataFrame()
    chunks = [users[x:x + 100] for x in range(0, len(users), 100)]  # Twitter API handles at most 100 users per request
    for chunk in chunks:
        success = False
        while not success:
            try:
                current_users = client.get_users(ids=chunk, user_fields=['created_at', 'verified', 'public_metrics'])
                success = True
            except Exception as e:
                print(e)
                time.sleep(11)  # Twitter API has rate limits that
        current_users_df = pd.DataFrame()
        for current_user in current_users.data:
            temp = pd.DataFrame({'author_id': current_user.id,
                                 'user_created_at': current_user.created_at,
                                 'followers': current_user.get('public_metrics').get('followers_count'),
                                 'following': current_user.get('public_metrics').get('following_count'),
                                 'tweet_count': current_user.get('public_metrics').get('tweet_count'),
                                 'verified': current_user.get('verified')}, index=[0])
            current_users_df = pd.concat([current_users_df, temp], ignore_index=True, axis=0)
        df_user_db = pd.concat([df_user_db, current_users_df], ignore_index=True, axis=0)

    return df_user_db
