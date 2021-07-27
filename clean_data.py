import pandas as pd

def get_data():
    # read tables
    classes = pd.read_csv('Monster_Classes.csv')
    g_data = pd.read_csv('MonsterHunter_General_Data.csv')
    m_games = pd.read_csv('Monsters_in_Games.csv')
    # re order table to create a column to join on
    monsters_in_games = m_games.melt(var_name='Title', value_name='Name')
    monsters_in_games = monsters_in_games[monsters_in_games['Name'].notnull()]
    # csv reads 'Na' as a NaN when supposed to be North America (Na)
    g_data['Country Released'] = g_data['Country Released'].fillna('North America')
    # Merge Tables
    df = pd.merge(classes, monsters_in_games, on='Name')
    mh_data = pd.merge(df, g_data, on='Title')
    # convert date column to a datetime object
    mh_data['Date Released'] = pd.to_datetime(mh_data['Date Released'])
    return mh_data