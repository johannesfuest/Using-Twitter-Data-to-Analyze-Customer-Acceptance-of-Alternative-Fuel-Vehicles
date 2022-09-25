import time
import tweepy as tw
import pandas as pd

# set up twitter api
api_key = "OwFAItbMkPAI4hLVoocO1qX79"
api_key_secret = "5jxBs7wFahIfyV3IfUshXpvCmCoOzHv96WbFSfOYBBR6Wf0CnT"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAP1ZdQEAAAAAd5hQaJkJ3EU9gGfMguy4h%2BUNMdg%3DyrOWYkstwTFquEnQZ74eg9dth00BQ3csG5bpnZxog9CZVofGiH"
client = tw.Client(bearer_token=bearer_token)
df_EV_EN = pd.DataFrame()
start_time = '2017-08-01T00:00:00Z'
end_time = '2022-08-01T00:00:00Z'
#queries for different DBs
ev_en_query = "(electric vehicles OR electric vehicle OR electric cars OR electric car OR e-cars OR e-car OR ecars OR ecar) -is:retweet -is:reply lang:en"
ev_de_query = "(electric vehicles OR electric vehicle OR electric cars OR electric car OR e-cars OR e-car OR ecars OR ecar OR e-autos OR e-auto OR eautos OR eauto OR efahrzeuge OR efahrzeug OR e-fahrzeuge OR e-fahrzeug OR elektroautos OR elektroauto) -is:retweet -is:reply lang:de"
sf_de_query = "(synthetic fuels OR synthetic fuel OR e-fuels OR e-fuel OR efuels OR efuel OR synfuels OR synfuel OR artificial fuels OR artifical fuel OR e-treibstoffe OR e-treibstoff OR etreibstoffe OR etreibstoff OR ekraftstoffe OR ekraftstoff OR e-kraftstoffe OR e-kraftstoff OR synthetische kraftstoffe OR synthetischer kraftstoff OR synthetischem Kraftstoff) -is:retweet -is:reply lang:de"
sf_en_query = "(synthetic fuels OR synthetic fuel OR e-fuels OR e-fuel OR efuels OR efuel OR synfuels OR synfuel OR artificial fuels OR artifical fuel) -is:retweet -is:reply lang:en"
tweet_fields = ['author_id', 'created_at', 'public_metrics', 'lang']

backup = False
while not backup:
    try:
        response = client.search_all_tweets(query=ev_en_query, max_results=500, tweet_fields=tweet_fields,
                                            start_time=start_time, end_time=end_time)
        backup = True
    except Exception as e:
        print(e)
        time.sleep(3)
for tweet in response.data:
    current_index = len(df_EV_EN.index)
    temp = pd.DataFrame({'tweet_id': tweet.get('id'), 'author_id': tweet.get('author_id'),
             'text': '"' + tweet.get('text').replace(",", "").replace(';', '').replace('\n',' ').replace('\r',' ').strip() + '"',
             'tweet_created_at': tweet.get('created_at'),
             'likes': tweet.data.get('public_metrics').get('like_count'),
             'comments': tweet.data.get('public_metrics').get('reply_count'),
             'retweets': tweet.data.get('public_metrics').get('retweet_count')}, index=[current_index])
    df_EV_EN = pd.concat([df_EV_EN, temp], ignore_index=True, axis=0)

while response.meta.get('next_token') is not None and len(df_EV_EN) < 500:
    print(len(df_EV_EN.index))
    print(df_EV_EN['tweet_created_at'].iat[-1])
    success = False
    while not success:
        try:
            response = client.search_all_tweets(query=ev_en_query, max_results=500, tweet_fields=tweet_fields,
                                                start_time=start_time, end_time=end_time, next_token=response.meta.get('next_token'))
            success = True
        except Exception as e:
            print(e)
            time.sleep(10)
    temp_add = pd.DataFrame()
    for tweet in response.data:
        current_index = len(df_EV_EN.index)
        temp = pd.DataFrame(
            {'tweet_id': tweet.get('id'), 'author_id': tweet.get('author_id'),
             'text': '"' + tweet.get('text').replace(",", "").replace(';', '').replace('\n',' ').replace('\r',' ').strip() + '"',
             'tweet_created_at': tweet.get('created_at'),
             'likes': tweet.data.get('public_metrics').get('like_count'),
             'comments': tweet.data.get('public_metrics').get('reply_count'),
             'retweets': tweet.data.get('public_metrics').get('retweet_count')}, index=[current_index])
        temp_add = pd.concat([temp_add, temp], ignore_index=True, axis=0)
    df_EV_EN = pd.concat([df_EV_EN, temp_add], ignore_index=True, axis=0)
df_EV_EN.to_csv('EV_EN_DB_addon.csv', index=False)