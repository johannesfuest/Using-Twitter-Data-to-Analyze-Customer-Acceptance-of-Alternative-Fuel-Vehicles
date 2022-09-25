import pandas as pd

parse_dates = ['user_created_at', 'tweet_created_at']
ev_de = pd.read_csv(('SF_DE_FINAL.csv'), dtype={"tweet_created_at": "string",
                                                "text": "string",
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
batteryterms = ['battery', 'batterie']
sustainabilityterms = ['sustainabl', 'cO2', 'sustainability', 'global warming', 'climate change', 'klima', 'nachhaltig', 'erderwärmung', 'umwelt']
rangeterms = ['range', 'ranges', 'distance', 'reichweite', 'fahrtweite', 'load', 'charging', 'charge', 'infrastructure', 'lade', 'infrastruktur', 'säule', 'wirkungsgrad', 'effizienz', 'effic', 'energy', 'energie']
costterms = ['cheap', 'expensive', 'price', 'cost', 'economical', 'economics', 'pay', 'zahlen', 'preis', 'teuer', 'teurer', 'kosten', 'kostet']
lindnerterms = ['Lindner', 'Porschegate']
EV_DE_batteries = ev_de[ev_de['text'].str.contains('|'.join(batteryterms))]
EV_DE_sustainability = ev_de[ev_de['text'].str.contains('|'.join(sustainabilityterms))]
EV_DE_range = ev_de[ev_de['text'].str.contains('|'.join(rangeterms))]
EV_DE_costs = ev_de[ev_de['text'].str.contains('|'.join(costterms))]
EV_DE_lindner = ev_de[ev_de['text'].str.contains('|'.join(lindnerterms))]

EV_DE_batteries.to_csv('SF_DE_BATTERY.csv', index=False)
EV_DE_sustainability.to_csv('SF_DE_SUSTAINABILITY.csv', index=False)
EV_DE_range.to_csv('SF_DE_RANGE.csv', index=False)
EV_DE_costs.to_csv('SF_DE_COSTS.csv', index=False)
EV_DE_lindner.to_csv('SF_DE_LINDNER.csv', index=False)




