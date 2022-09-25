import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import numpy as np

name = 'SF_DE_LINDNER'
parse_dates = ['user_created_at', 'tweet_created_at']
df = pd.read_csv((name + '.csv'), dtype={"tweet_created_at": "string",
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
print('Dataframe read.')
df_agg = pd.read_csv((name + '_agg.csv'), dtype={"year": 'string',
                                                 'month': 'string',
                                                 'total_tweets': 'int64',
                                                 'negative': 'float64',
                                                 'neutral': 'float64',
                                                 'positive': 'float64',
                                                 })
print('aggregated df read')
df['follower_percentile'] = df.followers.rank(pct=True)
df.follower_percentile = df.follower_percentile.round(4)
df['likes_percentile'] = df.likes.rank(pct=True)
df.likes_percentile = df.likes_percentile.round(4)
df['retweets_percentile'] = df.retweets.rank(pct=True)
df.retweets_percentile = df.retweets_percentile.round(4)
df['comments_percentile'] = df.comments.rank(pct=True)
df.comments_percentile = df.comments_percentile.round(4)
df['tweet_count_percentile'] = df.tweet_count.rank(pct=True)
df.tweet_count_percentile = df.tweet_count_percentile.round(4)
df['engagement_score'] = df['likes_percentile'] + df['retweets_percentile'] + df['comments_percentile']
df['engagement_percentile'] = df.engagement_score.rank(pct=True)
df.engagement_percentile = df.engagement_percentile.round(4)

df_agg_followers = df.groupby(['follower_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))
df_agg_likes = df.groupby(['likes_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))
df_agg_comments = df.groupby(['comments_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))
df_agg_retweets = df.groupby(['retweets_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))
df_agg_tweetcount = df.groupby(['tweet_count_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))
df_agg_engagement = df.groupby(['engagement_percentile'])\
    .agg(positive=('positive', 'mean'),
         neutral=('neutral', 'mean'),
         negative=('negative', 'mean'),
         number= ('tweet_created_at', 'count'))


maxfollowers = df['followers'].loc[df['followers'].idxmax()]
oldestuser = df['user_created_at'].loc[df['user_created_at'].idxmin()]
maxlikes = df['likes'].loc[df['likes'].idxmax()]
maxcomments = df['comments'].loc[df['comments'].idxmax()]
maxretweets = df['retweets'].loc[df['retweets'].idxmax()]
maxtweetcount = df['tweet_count'].loc[df['tweet_count'].idxmax()]

print('Maximum number of followers: ' + str(maxfollowers))
print('Maximum number of likes: ' + str(maxlikes))
print('Maximum number of tweets per user: ' + str(maxtweetcount))
print('Maximum number of comments: ' + str(maxcomments))
print('Maximum number of retweets: ' + str(maxretweets))
print('Oldest user was created on: ' + str(oldestuser))

font = {'family': 'DejaVu Sans',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }

#overall sentiment distribution
x = (df['positive']/(df['positive'] + df['negative']))
plt.hist(x, bins=100, ec='black', color='b')
plt.ylabel('Number of Tweets', fontdict=font)
plt.xlabel('Relative Sentiment Positivity', fontdict=font)
plt.title('Tweet Sentiment Distribution in ' + name)
tickvalues = [0.25,0.75]
plt.xticks(tickvalues, ['← Less Positive', 'More Positive →'])
plt.show()

# sentiment over time
x = pd.to_datetime(df_agg['year'].astype(str) + df_agg['month'].astype(str), format='%Y%m')
plt.stackplot(x, df_agg['positive'], df_agg['neutral'], df_agg['negative'], ec='black', colors=['g', 'b', 'r'])
plt.title('Sentiment Distribution in ' + name)
plt.ylabel('Average Tweet Sentiment', fontdict=font)
plt.legend(loc='lower right', labels=['positive', 'neutral', 'negative'], bbox_to_anchor=(1.12, 0), fontsize=6)
plt.box(on=False)
tickvalues = [0, 0.25, 0.5, 0.75, 1]
plt.yticks(tickvalues, ['0%', '25%', '50%', '75%', '100%'], rotation='horizontal')
plt.show()

# tweet volume over time
x = pd.to_datetime(df_agg['year'].astype(str) + df_agg['month'].astype(str), format='%Y%m')
y = df_agg['total_tweets']
plt.title('Tweet Volumes Over Time in ' + name)
plt.xlabel('Date', fontdict=font)
plt.ylabel('Number of Tweets', fontdict=font)
plt.bar(x, y, width=16.0, ec='black', color='b')
plt.show()

#positivity vs engagement
x = df_agg_engagement.index
y = df_agg_engagement['positive'] / (df_agg_engagement['positive'] + df_agg_engagement['negative'])
plt.scatter(x, y, marker='o', color='b', s=df_agg_engagement['number'] / 10000)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Engagement Percentile', fontdict=font)
plt.ylabel('Relative Sentiment Positivity', fontdict=font)
plt.title('Engagement and Positivity in  ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Positive', 'More Positive →'], rotation='vertical')
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()

#neutrality vs engagement
x = df_agg_engagement.index
y = df_agg_engagement['neutral']
plt.scatter(x, y, marker='o', color='b', s=df_agg_engagement['number'] / 100)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Engagement Percentile', fontdict=font)
plt.ylabel('Average Tweet Neutrality', fontdict=font)
plt.title('Engagement and Neutrality in ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Neutral', 'More Neutral →'], rotation='vertical')
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()


# positivity vs followers
x = df_agg_followers.index
y = df_agg_followers['positive'] / (df_agg_followers['positive'] + df_agg_followers['negative'])
plt.scatter(x, y, marker='o', color='b', s=df_agg_followers['number'] / 100)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Followers Percentile', fontdict=font)
plt.ylabel('Relative Sentiment Positivity', fontdict=font)
plt.title('Followers and Positivity in ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Positive', 'More Positive →'], rotation='vertical')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()

#neutrality vs followers
x = df_agg_followers.index
y = df_agg_followers['neutral']
plt.scatter(x, y, marker='o', color='b', s=df_agg_followers['number'] / 100)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Number of Followers Percentile', fontdict=font)
plt.ylabel('Neutrality of Tweets', fontdict=font)
plt.title('Followers and Neutrality in ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Neutral', 'More Neutral →'], rotation='vertical')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()

#positivity vs tweet count
x = df_agg_tweetcount.index
y = df_agg_tweetcount['positive'] / (df_agg_tweetcount['positive'] + df_agg_tweetcount['negative'])
plt.scatter(x, y, marker='o', color='b', s=df_agg_tweetcount['number'] / 100)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Tweet Count Percentile', fontdict=font)
plt.ylabel('Average Sentiment Positivity', fontdict=font)
plt.title('User Activity and Positivity in ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Positive', 'More Positive →'], rotation='vertical')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()

#neutrality vs tweet count
x = df_agg_tweetcount.index
y = df_agg_tweetcount['neutral']
plt.scatter(x, y, marker='o', color='b', s=df_agg_tweetcount['number'] / 100)
plt.ylim([0, 1])
plt.xlim([0, 1])
plt.xlabel('Tweet Count Percentile', fontdict=font)
plt.ylabel('Neutrality of Tweets', fontdict=font)
plt.title('User Activity and Neutrality in ' + name)
p1 = np.polyfit(x, y, 1)
x_low = 0.0
x_high = 1.0
x_extended = np.linspace(x_low, x_high, 100)
plt.plot(x_extended, np.polyval(p1,x_extended),'r-')
tickvalues = [0.25,1]
plt.yticks(tickvalues, ['← Less Neutral', 'More Neutral →'], rotation='vertical')
res = stats.pearsonr(x, y)
plt.figtext(0.65, 0.15, 'Correlation: ' + str("{:.4f}".format(round(res.statistic, 4))) + '\np-Value: ' + "{:.4f}".format(round(res.pvalue, 4)))
plt.show()

