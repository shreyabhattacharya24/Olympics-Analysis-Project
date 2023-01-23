import pandas as pd
def preprocess():
    athlete = pd.read_csv('athlete_events.csv')
    regions = pd.read_csv('noc_regions.csv')
    athlete = athlete[athlete['Season'] == 'Summer']
    athlete = athlete.merge(regions, on='NOC', how='left')
    athlete.drop_duplicates(inplace=True)
    athlete = pd.concat([athlete, pd.get_dummies(athlete['Medal'])], axis=1)

    return athlete

