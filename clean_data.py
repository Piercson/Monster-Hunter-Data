import pandas as pd

def get_data():
    classes = pd.read_csv('Monster_Classes.csv')
    g_data = pd.read_csv('MonsterHunter_General_Data.csv')
    m_games = pd.read_csv('Monsters_in_Games.csv')
    monsters_in_games = m_games.melt(var_name='Title', value_name='Name')
    monsters_in_games = monsters_in_games[monsters_in_games['Name'].notnull()]
    g_data['Country Released'] = g_data['Country Released'].fillna('North America')
    df = pd.merge(classes, monsters_in_games, on='Name')
    mh_data = pd.merge(df, g_data, on='Title')
    mh_data['Date Released'] = pd.to_datetime(mh_data['Date Released'])
    return mh_data