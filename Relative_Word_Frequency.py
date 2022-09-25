import operator
import pandas as pd


name = 'EV_DE_DB'
parse_dates = ['tweet_created_at']
df = pd.read_csv((name + '.csv'), dtype={'tweet_id': 'string',
                                         'author_id': 'string',
                                         'text': 'string',
                                         'tweet_created_at': 'string',
                                         'likes': 'int64',
                                         'commments': 'int64',
                                         'retweets': 'int64'},
                 parse_dates=parse_dates)
df['year'] = df['tweet_created_at'].dt.year
df['month'] = df['tweet_created_at'].dt.month.map("{:02}".format)
df['final_date'] = pd.to_datetime(df['year'].astype(str) + df['month'].astype(str), format='%Y%m')
df.drop('tweet_created_at', axis=1)
df.drop('year', axis=1)
df.drop('month', axis=1)
total_tweets = len(df.index)

df_agg = df.groupby(['final_date'], as_index=False).agg({'text': ' '.join, 'tweet_id': 'count'})
df_agg['total_tweets'] = df_agg['tweet_id']
df_agg.drop('tweet_id', inplace=True, axis=1)


print('Dataframe read successfully with length ' + str(total_tweets))
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZäüöß')
all_words = []
#build frequency of word per tweet overall
overall_word_frequency = {}
for index, row in df.iterrows():
    text = row['text']
    text = ''.join(filter(whitelist.__contains__, text))
    text = text.lower()
    text = text.split(' ')
    for word in text:
        if word in overall_word_frequency:
            overall_word_frequency[word] += 1
        else:
            overall_word_frequency[word] = 1
            all_words.append(word)
    if(index%10000 == 0):
        print(index)
for word in all_words:
    overall_word_frequency[word] = overall_word_frequency[word] / total_tweets

def getTop10Words(row_text, tweetspermonth):
    row_word_frequency = {}
    for words in all_words:
        row_word_frequency[words] = 0
    row_text = ''.join(filter(whitelist.__contains__, row_text)).lower().split(' ')
    for words in row_text:
        if not 'https' in words:
            row_word_frequency[words] += 1
    for words in all_words:
        if row_word_frequency[words] > 50:
            row_word_frequency[words] = row_word_frequency[words] / tweetspermonth
        else:
            row_word_frequency[words] = 0
    for words in all_words:
        row_word_frequency[words] = row_word_frequency[words] / overall_word_frequency[words]
    top10 = dict(sorted(row_word_frequency.items(), key=operator.itemgetter(1), reverse=True)[:20])
    returner = ''
    for words in top10:
        returner += words + ', '
    return returner


df_agg['topwords'] = ''

for index, row in df_agg.iterrows():
    topwords = getTop10Words(row['text'], row['total_tweets'])
    df_agg.topwords.iloc[[index]] = topwords

df_agg.drop('text', inplace=True, axis=1)
df_agg.to_csv(name + '_wordfreq.csv')







