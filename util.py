import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def choose_race(name, lastname_race_df):
    """
    given a name (with no spaces), randomly choose a race given the probabilities
    in the the name-to-likelihood mapping provided in lastname_race_df
    """
    np.random.seed = 42
    
    races = ['white', 'black', 'asian', 'aian', 'mix', 'hispanic']
    probabilities = lastname_race_df.loc[lastname_race_df['lastname']==name, races].values[0]
    
    # normalize so that probabilities add to 1
    probabilities /= probabilities.sum()
    
    # if name is more than 80% likely to be a race, then just use that race, otherwise, sample
    race = [races[i] for (i, p) in enumerate(probabilities>0.8) if p == True]
    if len(race) > 0:
        return race[0]
    else:
        return np.random.choice(races, p=probabilities)

def get_race_dist_of_lastname():
    # read in data
    lastname_race_df = pd.read_json('lastnames.json')

    # set columns to first row 
    lastname_race_df.columns = [
        'lastname', 
        'rank', 
        'count', 
        'white', 
        'asian', 
        'mix', 
        'aian', 
        'black', 
        'hispanic']

    # skip first and last rows
    lastname_race_df = lastname_race_df.iloc[1:-1]

    # drop unwanted columns
    lastname_race_df = lastname_race_df.drop(['rank', 'count'], axis=1)

    # lowercase names
    lastname_race_df['lastname'] = lastname_race_df['lastname'].str.lower()

    # transform race percentage to a probability
    races = ['white', 'black', 'asian', 'aian', 'mix', 'hispanic']
    lastname_race_df[races] = lastname_race_df[races].replace({'(S)': 0}).apply(lambda x: pd.to_numeric(x)/100)
    
    return lastname_race_df


def get_race_from_full_name(name, race, lastname_race_df):
    """
    starting from the end, check the word against the lastname_race_df to see that it 
    exist. If so, choose a race using the 'choose_race' function, otherwise, check the
    next word.
    Example:
        "Millie Bobby Brown"
        --> choose race for 'Brown'
        --> if not found, choose race for 'Bobby'
        --> if not found, choose race for 'Millie'
    """  
    if race == "asian" or race == "indian":
        return race
    
    if name is None or len(name) <= 1:
        return None
    
    name = name.lower()

    split_array = name.rsplit(' ', 1)
    last = split_array[-1]
    remaining = None

    if len(split_array) > 1:
        remaining = split_array[0]
        
    try:
        return choose_race(last, lastname_race_df)
    except Exception as e:
        return get_race_from_full_name(remaining, race, lastname_race_df)
    

def plot_distribution(dist_df, title, ax, kind='bar', show_pct=True):
    """
    Plot distribution as a bargraph
    If dropna==false, highlight NaNs
    Print percentage of each value in distribution
    """
    ax = dist_df.plot(
        kind=kind, 
        title=title,
        ax=ax)
    
    # highlight NaNs if not dropped
    try:
        ax.patches[dist_df.index.get_loc(None)].set_facecolor('red')
    except Exception as e:
        pass
    
    if show_pct:
        normalized_dist_df = dist_df.div(dist_df.values.sum())
        pct_dist = np.multiply(list(normalized_dist_df), 100)
        for i, val in enumerate(dist_df):
            ax.text(i, val + (0.01 * val), str('%.2f %%' % pct_dist[i])) 