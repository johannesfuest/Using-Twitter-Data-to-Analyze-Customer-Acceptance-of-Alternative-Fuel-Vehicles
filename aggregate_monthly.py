import pandas as pd


def aggregate_monthly(dfs, names):
    """
    Creates and saves a list of dataframes that aggregate the data contained in each tweet data dataframe in dfs.
    :param dfs: A list of dataframes containing tweet data
    :param names: A list of names of the dataframes in dfs
    :return: A list of aggregated dataframes corresponding to each dataframe in df. Contain one row per month.
    """

    agg_dfs = []
    for i in range(len(dfs)):
        dfs[i]['year'] = dfs[i]['tweet_created_at'].dt.year
        dfs[i]['month'] = dfs[i]['tweet_created_at'].dt.month.map("{:02}".format)
        df_aggregated = dfs[i].groupby(['year', 'month']) \
            .agg(total_tweets=('tweet_created_at', 'count'),
                 positive=('positive', 'mean'),
                 neutral=('neutral', 'mean'),
                 negative=('negative', 'mean'))
        df_aggregated.to_csv(names[i] + '_agg.csv')
        agg_dfs.append(df_aggregated)
    return agg_dfs

