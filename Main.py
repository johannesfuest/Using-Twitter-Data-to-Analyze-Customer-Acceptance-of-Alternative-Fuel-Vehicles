import aggregate_monthly
import chart_creator
import datetime
import pandas as pd
import tweet_Database_Creator
import user_db_creator
import sentiment_analysis
import subtopic_filtering
import sys
import trending_words

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage:")
        print("    <lang> <bearer_token> <ev_bool> <filename> <start_date> <end_date>")
        sys.exit(1)

    # Set up twitter api
    lang = sys.argv[1]
    bearer_token = sys.argv[2]

    # Set database type
    ev = bool(sys.argv[3])

    # Set start and end date of query (defaults to the past five years)
    if len(sys.argv) == 7:
        start_date = datetime.datetime.strptime(sys.argv[5], '%m-%d-%Y').date()
        end_date = datetime.datetime.strptime(sys.argv[6], '%m-%d-%Y').date()

    else:
        start_date = datetime.datetime.today() - datetime.timedelta(days=365)
        end_date = datetime.datetime.today()

    # Generate database
    df = tweet_Database_Creator.create_databases(True, sys.argv[1], start_date, end_date, bearer_token)
    print('Tweet database successfully generated.')

    # Perform sentiment analysis
    df = sentiment_analysis.process_df(df)
    print('Sentiment analysis complete.')

    # Get users database
    df_users = user_db_creator.create_user_db(bearer_token, df)
    print('User database complete.')

    # Add user data to main dataframe and save final database
    final_df = pd.merge(df, df_users, left_on='author_id', right_on ='author_id', how='inner')
    final_df.to_csv(sys.argv[4] + '.csv', index=False)
    print('Final dataframe saved.')

    # Generate subtopic dataframes and add to list
    all_dfs, names = [final_df, subtopic_filtering.generate_subtopic_dfs(final_df, sys.argv[4])]

    # Generate trending words dataframes
    for i in range(len(all_dfs)):
        trending_words.generate_trending_words(all_dfs[i], names[i])
    print('Trending words for all dataframes computed and saved.')

    # Generate monthly aggregated dataframes
    agg_dfs = aggregate_monthly.aggregate_monthly(all_dfs, names)
    print('All dataframes aggregated.')

    # Create and save charts for all dataframes
    chart_creator.create_charts(all_dfs, agg_dfs, names)
    print('All charts successfully generated and saved.')
    sys.exit(0)
