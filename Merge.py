import pandas as pd

#this code joins the results of the sentiment analysis with the user data

db_df = pd.read_csv('SF_DE_DB_sentiment.csv')
users_df = pd.read_csv('user_db.csv')
final_df = pd.merge(db_df, users_df, left_on='user_id', right_on ='user_id', how='inner')
final_df.to_csv('SF_DE_FINAL.csv', index=False)