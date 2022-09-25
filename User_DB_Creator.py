import time
import pandas as pd
import tweepy as tw

#set up twitter api
api_key = "2sKwDO2tlAJiq11LC7whEfukQ"
api_key_secret = "6KD6XnElawxBUuxifO2oVC8KSZRXfFGF2dpsdC8KqRBv63QMYr"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAH0eewEAAAAA3krQAuvYWofuhBtnz8IYoTkwNUA%3DAihYMytVkLHAvfGptVEhod95LZsBQHBqbWM72Jhj4x6AIntm7I"
client = tw.Client(bearer_token = bearer_token)
#create list of users from tweet database
parse_dates = ['tweet_created_at']
users1 = pd.read_csv('EV_EN_DB.csv', dtype={"tweet_id": "string", "author_id": "string", "text": "string", "tweet_created_at": "string", "lang": "string", "likes": "string", "comments": "string", "retweets": "string"}, parse_dates=parse_dates, lineterminator='\n')
users2 = pd.read_csv('EV_DE_DB.csv', dtype={"tweet_id": "string", "author_id": "string", "text": "string", "tweet_created_at": "string", "lang": "string", "likes": "string", "comments": "string", "retweets": "string"}, parse_dates=parse_dates, lineterminator='\n')
users3 = pd.read_csv('SF_EN_DB.csv', dtype={"tweet_id": "string", "author_id": "string", "text": "string", "tweet_created_at": "string", "lang": "string", "likes": "string", "comments": "string", "retweets": "string"}, parse_dates=parse_dates, lineterminator='\n')
users4 = pd.read_csv('SF_DE_DB.csv', dtype={"tweet_id": "string", "author_id": "string", "text": "string", "tweet_created_at": "string", "lang": "string", "likes": "string", "comments": "string", "retweets": "string"}, parse_dates=parse_dates, lineterminator='\n')
print('data read')
users = pd.concat([users1, users2, users3, users4 ], ignore_index=True)
users = users[users['author_id'] != '']
users = list(set(users['author_id'].tolist()))
users = list(filter(None, users))
users = list(map(int,users))
print("total number of distinct users:")
print(len(users))
#generate user db
df_user_db = pd.DataFrame()
chunks = [users[x:x+100] for x in range(0, len(users), 100)]
for chunk in chunks:
    success = False
    while not success:
        try:
            currentusers = client.get_users(ids=chunk, user_fields=['created_at', 'verified', 'public_metrics'])
            success = True
        except Exception as e:
            print(e)
            time.sleep (11)
    currentusers_df = pd.DataFrame()
    for currentuser in currentusers.data:
        temp = pd.DataFrame({'user_id': currentuser.id,
                             'user_created_at': currentuser.created_at,
                             'followers': currentuser.get('public_metrics').get('followers_count'),
                             'following': currentuser.get('public_metrics').get('following_count'),
                             'tweet_count': currentuser.get('public_metrics').get('tweet_count'),
                             'verified': currentuser.get('verified')}, index=[0])
        currentusers_df = pd.concat([currentusers_df, temp], ignore_index=True, axis=0)
    df_user_db = pd.concat([df_user_db, currentusers_df], ignore_index=True, axis=0)
    print(len(df_user_db.index))
df_user_db.to_csv('user_db.csv', index=False)