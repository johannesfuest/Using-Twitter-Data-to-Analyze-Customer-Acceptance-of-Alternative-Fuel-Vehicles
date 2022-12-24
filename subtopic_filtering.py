import pandas as pd


def generate_subtopic_dfs(df, filename):
    """
    Takes a dataframe and generates and saves and returns dataframes that filter by search terms relateed to subtopics
    :param filename: Prefix of the desired file name
    :param df: A dataframe containing tweet data
    :return: A list of dataframes that include tweets filtered by subtopics
    """

    # Lists of subtopic strings
    battery_terms = ['battery', 'batterie']
    sustainability_terms = ['sustainable', 'cO2', 'sustainability', 'global warming', 'climate change', 'klima',
                            'nachhaltig', 'erderwärmung', 'umwelt']
    range_terms = ['range', 'ranges', 'distance', 'reichweite', 'fahrtweite', 'load', 'charging', 'charge',
                   'infrastructure', 'lade', 'infrastruktur', 'säule', 'wirkungsgrad', 'effizienz', 'effic', 'energy',
                   'energie']
    cost_terms = ['cheap', 'expensive', 'price', 'cost', 'economical', 'economics', 'pay', 'zahlen', 'preis', 'teuer',
                  'teurer', 'kosten', 'kostet']
    lindner_terms = ['Lindner', 'Porschegate']

    # Create dataframes by filtering original dataframe.
    batteries = df[df['text'].str.contains('|'.join(battery_terms))]
    sustainability = df[df['text'].str.contains('|'.join(sustainability_terms))]
    range = df[df['text'].str.contains('|'.join(range_terms))]
    costs = df[df['text'].str.contains('|'.join(cost_terms))]
    lindner = df[df['text'].str.contains('|'.join(lindner_terms))]

    # Generate name list for later use
    names = [filename, filename + '_batteries', filename + 'sustainability', filename + '_range', filename + '_costs',
             filename + '_lindner']

    # Save subtopic dataframes to csv
    batteries.to_csv(filename + '_batteries.csv', index=False)
    sustainability.to_csv(filename + '_sustainability.csv', index=False)
    range.to_csv(filename + '_range.csv', index=False)
    costs.to_csv(filename + '_costs.csv', index=False)
    lindner.to_csv(filename + '_lindner.csv', index=False)

    # Return dataframes as list
    return [batteries, sustainability, range, costs, lindner], names
