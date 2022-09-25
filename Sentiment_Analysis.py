from threading import Thread

from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd

def process_df(name, lang):
    def complex_function(tweet):
        tweet_words = []
        for word in tweet.split(' '):
            if word.startswith('@') and len(word) > 1:
                word = 'user'
            elif word.startswith('http'):
                word = 'http'
            tweet_words.append(word)
        tweet_processed = " ".join(tweet_words)
        # perform sentiment analysis
        encoded_tweet = tokenizer(tweet_processed, return_tensors='pt')
        try:
            output = model(**encoded_tweet)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
        except Exception as e:
            print(e)
            scores = [-1, -1, -1]
        return f"{scores[0]},{scores[1]},{scores[2]}"
    #set up model and tokenizer
    if lang == 'en':
        roberta = 'cardiffnlp/twitter-roberta-base-sentiment'
    else:
        roberta = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    print('model'+ roberta + ' downloaded and tokenizer built')

    #load tweet database
    parse_dates = ['tweet_created_at']
    print('thread started for ' + name)
    df = pd.read_csv(name + '.csv', sep=',',
                     dtype={"tweet_id": "string", "author_id": "string", "text": "string", "tweet_created_at": "string",
                            "lang": "string", "likes": "int64", "comments": "int64", "retweets": "int64"},
                     parse_dates=parse_dates, engine='python')
    print(name + ' read successfully')
    tqdm.pandas()
    # iterate over tweets
    df["results"] = df["text"].progress_apply(complex_function)
    df[["negative", "neutral", "positive"]] = df.results.str.split(',', expand=True)
    df.drop('results', inplace=True, axis=1)
    df["negative"] = pd.to_numeric(df["negative"])
    df["neutral"] = pd.to_numeric(df["neutral"])
    df["positive"] = pd.to_numeric(df["positive"])
    df["user_id"] = df["author_id"]
    df = df[["tweet_created_at", "user_id", "text", "negative", "neutral", "positive", "likes", "comments", "retweets"]]
    df = df[(df.positive >= 0) & (df.positive <= 1)]
    df.to_csv(name + '_sentiment.csv')
    return


if __name__ == "__main__":
    print("sentiment analysis initiated")
    dfs = ['EV_EN_DB', 'SF_EN_DB']
    dfs_de = ['EV_DE_DB', 'SF_DE_DB']
    for name in dfs:
        t = Thread(target=process_df, args=(name, 'en'))
        t.start()
    for name in dfs_de:
        t = Thread(target=process_df, args=(name, 'de'))
        t.start()

