import pandas as pd

name = 'SF_DE_LINDNER'
parse_dates = ['user_created_at', 'tweet_created_at']
df = pd.read_csv((name+'.csv'), dtype={"tweet_created_at": "string",
                                           "likes": "int64",
                                           "comments": "int64",
                                           "retweets": "int64",
                                           "negative": "float64",
                                           "neutral": "float64",
                                           "positive": "float64",
                                           "followers": "int64",
                                           "following": "int64",
                                           "tweet_count": "int64",
                                           "verified": "bool",
                                           "user_created_at": "string"},
                 parse_dates=parse_dates)
df['year'] = df['tweet_created_at'].dt.year
df['month'] = df['tweet_created_at'].dt.month.map("{:02}".format)

df_aggregated = df.groupby(['year', 'month'])\
    .agg(total_tweets=('tweet_created_at', 'count'),
         positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'))
df_aggregated.to_csv(name+'_agg.csv')
