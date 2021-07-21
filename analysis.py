import pandas as pd
import numpy as np
import helpers

# returns the amount analysis titles with columns Base and Ultimate
def get_amt_titles_df():
    return pd.DataFrame(
    {"Base": pd.Series(['Monster Hunter','Monster Hunter Freedom 2', 'Monster Hunter 3', 'Monster Hunter Portable 3rd',
              'Monster Hunter 4','Monster Hunter Generations', 'Monster Hunter: World', 'Monster Hunter Rise',]),
     "Ultimate": pd.Series(['Monster Hunter Freedom', 'Monster Hunter Freedom Unite', 'Monster Hunter 3 Ultimate', np.nan,
            'Monster Hunter 4 Ultimate', 'Monster Hunter Generations Ultimate', 'Monster Hunter World: Iceborne', np.nan,])})

def get_amt_table(amt_analysis_titles, titles_amt_data):
    # filter for analysis Titles
    amt_monsters_df = pd.DataFrame(
        columns=['Title', 'Release Date', 'Total Monsters', 'Large Monsters', 'Small Monsters',
                 'New Monsters', 'New Large Monsters', 'New Small Monsters', 'Variant Monsters'])
    valid_titles = titles_amt_data['Title'].unique()
    for title in valid_titles:
        title_data = titles_amt_data[titles_amt_data['Title'] == title]
        title_date = min(title_data['Date Released'])

        monsters_from_prev_games = titles_amt_data[titles_amt_data['Date Released'] < title_date][
            'Name'].drop_duplicates()
        monsters_in_title = title_data[['Name', 'Type', 'Size']].drop_duplicates()
        new_monsters = monsters_in_title[monsters_in_title['Name'].isin(monsters_from_prev_games) == False]
        num_variants = monsters_in_title[monsters_in_title['Size'] == 'Large']['Name'].count() - len(
            helpers.filter_out_variants(monsters_in_title[monsters_in_title['Size'] == 'Large']))
        try:
            new_large_t_monsters = new_monsters.groupby(['Size']).size().Large
        except:
            new_large_t_monsters = 0
        try:
            new_small_t_monsters = new_monsters.groupby(['Size']).size().Small
        except:
            new_small_t_monsters = 0

        df_segment = pd.DataFrame(
            [[title,
              title_date,
              monsters_in_title['Name'].count(),
              monsters_in_title.groupby(['Size']).size().Large,
              monsters_in_title.groupby(['Size']).size().Small,
              new_monsters['Name'].count(),
              new_large_t_monsters,
              new_small_t_monsters,
              num_variants]],
            columns=['Title', 'Release Date', 'Total Monsters', 'Large Monsters', 'Small Monsters',
                     'New Monsters', 'New Large Monsters', 'New Small Monsters', 'Variant Monsters'])
        amt_monsters_df = pd.concat([amt_monsters_df, df_segment])

    amt_monsters_df = amt_monsters_df.sort_values(by=['Release Date']).reset_index(drop=False)
    amt_monsters_df['New Monster Ratio'] = amt_monsters_df['New Large Monsters'] / amt_monsters_df['Large Monsters']
    amt_monsters_df['Variant Monster Ratio'] = amt_monsters_df['Variant Monsters'] / amt_monsters_df['Large Monsters']
    return amt_monsters_df

def get_base_ultimate_titles():
    return pd.DataFrame(
    {"Base": pd.Series(['Monster Hunter','Monster Hunter Freedom 2', 'Monster Hunter 3',
              'Monster Hunter 4','Monster Hunter X', 'Monster Hunter: World',]),
     "Ultimate": pd.Series(['Monster Hunter G', 'Monster Hunter Freedom Unite', 'Monster Hunter 3 Ultimate',
            'Monster Hunter 4 G', 'Monster Hunter XX', 'Monster Hunter World: Iceborne'])})
def get_base_ultimate_df(game_titles, mh_data):
    game_titles_lst = game_titles['Base'].append(game_titles['Ultimate']).dropna()
    game_title_data = mh_data[mh_data['Title'].isin(game_titles_lst) == True]
    game_title_data = game_title_data[['Title', 'Date Released']].sort_values(by=['Date Released']).drop_duplicates(
        subset=['Title'], keep='first')

    base = pd.merge(game_title_data, game_titles, left_on='Title', right_on="Base", how='right').dropna()[
        ['Title', 'Date Released']]
    ultimate = pd.merge(game_title_data, game_titles, left_on='Title', right_on="Ultimate", how='left').dropna()[
        ['Title', 'Date Released']]
    base = base.reset_index(drop=True).reset_index()
    ultimate = ultimate.reset_index(drop=True).reset_index()
    base['Large Monsters'] = base['Title'].apply(lambda title:
                                                 len(mh_data[
                                                         (mh_data['Title'] == title) & (mh_data['Size'] == 'Large')][
                                                         'Name'].unique()))
    ultimate['Large Monsters'] = ultimate['Title'].apply(lambda title:
                                                         len(mh_data[(mh_data['Title'] == title) & (
                                                                     mh_data['Size'] == 'Large')]['Name'].unique()))
    game_date_data = pd.merge(base, ultimate, on='index', suffixes=('_base', '_ultimate'))
    game_date_data
    game_date_data['date_difference'] = abs(
        game_date_data['Date Released_ultimate'] - game_date_data['Date Released_base'])
    game_date_data['monster_difference'] = abs(
    game_date_data['Large Monsters_ultimate'] - game_date_data['Large Monsters_base'])

    return game_date_data.drop('index',axis=1)