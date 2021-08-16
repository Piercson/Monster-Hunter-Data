import pandas as pd
import numpy as np
from src import helpers

# returns the amount analysis titles with columns Base and Ultimate
def get_amt_titles_df():
    return pd.DataFrame(
    {"Base": pd.Series(['Monster Hunter','Monster Hunter Freedom 2', 'Monster Hunter 3', 'Monster Hunter Portable 3rd',
              'Monster Hunter 4','Monster Hunter Generations', 'Monster Hunter: World', 'Monster Hunter Rise',]),
     "Ultimate": pd.Series(['Monster Hunter Freedom', 'Monster Hunter Freedom Unite', 'Monster Hunter 3 Ultimate', np.nan,
            'Monster Hunter 4 Ultimate', 'Monster Hunter Generations Ultimate', 'Monster Hunter World: Iceborne', np.nan,])})

def get_base_ultimate_titles():
    return pd.DataFrame(
    {"Base": pd.Series(['Monster Hunter','Monster Hunter Portable 2nd', 'Monster Hunter 3',
              'Monster Hunter 4','Monster Hunter X', 'Monster Hunter: World',]),
     "Ultimate": pd.Series(['Monster Hunter G', 'Monster Hunter Portable 2nd G', 'Monster Hunter 3 G',
            'Monster Hunter 4 G', 'Monster Hunter XX', 'Monster Hunter World: Iceborne'])})

def get_amt_table(amt_analysis_titles, mh_data):
    # Create blank output df
    amt_analysis_titles_lst = amt_analysis_titles['Base'].append(amt_analysis_titles['Ultimate']).dropna()
    titles_amt_data = mh_data[mh_data['Title'].isin(amt_analysis_titles_lst) == True]
    amt_monsters_df = pd.DataFrame(
        columns=['Title', 'Release Date', 'Total Monsters', 'Large Monsters', 'Small Monsters',
                 'New Monsters', 'New Large Monsters', 'New Small Monsters', 'Variant Monsters'])
    valid_titles = titles_amt_data['Title'].unique()
    # concat to tables for every analysis title
    for title in valid_titles:
        title_data = titles_amt_data[titles_amt_data['Title'] == title]
        title_date = min(title_data['Date Released'])
        # get monsters from previous games
        monsters_from_prev_games = titles_amt_data[titles_amt_data['Date Released'] < title_date][
            'Name'].drop_duplicates()
        # get monsters from current title
        monsters_in_title = title_data[['Name', 'Type', 'Size']].drop_duplicates()
        # get new monsters introduced in title
        new_monsters = monsters_in_title[monsters_in_title['Name'].isin(monsters_from_prev_games) == False]
        # get variant monsters
        num_variants = monsters_in_title[monsters_in_title['Size'] == 'Large']['Name'].count() - len(
            helpers.filter_out_variants(monsters_in_title[monsters_in_title['Size'] == 'Large']))
        # if there is new large monsters, add count otherwise it is 0.
        # repeated for new small monsters
        try:
            new_large_t_monsters = new_monsters.groupby(['Size']).size().Large
        except:
            new_large_t_monsters = 0
        try:
            new_small_t_monsters = new_monsters.groupby(['Size']).size().Small
        except:
            new_small_t_monsters = 0
        # concat row
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

    # compute ratios
    amt_monsters_df = amt_monsters_df.sort_values(by=['Release Date']).reset_index(drop=False)
    amt_monsters_df['New Monster Ratio'] = amt_monsters_df['New Large Monsters'] / amt_monsters_df['Large Monsters']
    amt_monsters_df['Variant Monster Ratio'] = amt_monsters_df['Variant Monsters'] / amt_monsters_df['Large Monsters']
    return amt_monsters_df


def get_base_ultimate_df(game_titles, mh_data):
    game_titles_lst = game_titles['Base'].append(game_titles['Ultimate']).dropna()
    game_title_data = mh_data[mh_data['Title'].isin(game_titles_lst) == True]
    game_title_data = game_title_data[['Title', 'Date Released']].sort_values(by=['Date Released']).drop_duplicates(
        subset=['Title'], keep='first')
    # make 2 tables, Base games and Ultimate games
    base = pd.merge(game_title_data, game_titles, left_on='Title', right_on="Base", how='right').dropna()[
        ['Title', 'Date Released']]
    ultimate = pd.merge(game_title_data, game_titles, left_on='Title', right_on="Ultimate", how='left').dropna()[
        ['Title', 'Date Released']]
    base = base.reset_index(drop=True).reset_index()
    ultimate = ultimate.reset_index(drop=True).reset_index()
    # add 'Large Monster' column to each table
    base['Large Monsters'] = base['Title'].apply(lambda title:
                                                 len(mh_data[
                                                         (mh_data['Title'] == title) & (mh_data['Size'] == 'Large')][
                                                         'Name'].unique()))
    base['Variant Monsters'] = base['Title'].apply(lambda title:
                                                   len(mh_data[
                                                           (mh_data['Title'] == title) & (mh_data['Size'] == 'Large')][
                                                           'Name'].unique()) - len(helpers.filter_out_variants(
                                                       mh_data[(mh_data['Title'] == title) & (
                                                                   mh_data['Size'] == 'Large')].drop_duplicates(
                                                           subset='Name'))))

    ultimate['Large Monsters'] = ultimate['Title'].apply(lambda title:
                                                         len(mh_data[(mh_data['Title'] == title) & (
                                                                 mh_data['Size'] == 'Large')]['Name'].unique()))
    ultimate['Variant Monsters'] = ultimate['Title'].apply(lambda title:
                                                           len(mh_data[
                                                                   (mh_data['Title'] == title) & (
                                                                               mh_data['Size'] == 'Large')][
                                                                   'Name'].unique()) - len(helpers.filter_out_variants(
                                                               mh_data[(mh_data['Title'] == title) & (
                                                                           mh_data['Size'] == 'Large')].drop_duplicates(
                                                                   subset='Name'))))
    # combine tables
    game_date_data = pd.merge(base, ultimate, on='index', suffixes=(' Base', ' Ultimate'))
    # compute date and monster differences
    game_date_data['Date Difference'] = abs(
        game_date_data['Date Released Ultimate'] - game_date_data['Date Released Base'])
    game_date_data['Monster Difference'] = abs(
        game_date_data['Large Monsters Ultimate'] - game_date_data['Large Monsters Base'])
    game_date_data['Variant Monster Difference'] = abs(
        game_date_data['Variant Monsters Ultimate'] - game_date_data['Variant Monsters Base'])

    return game_date_data.drop('index',axis=1)

def get_monster_occurance_df(analysis_titles, mh_data):
    # filter for analysis titles
    amt_analysis_titles_lst = analysis_titles['Base'].append(analysis_titles['Ultimate']).dropna()
    monster_occurance_data = mh_data[mh_data['Title'].isin(amt_analysis_titles_lst) == True].sort_values(
        by=['Date Released']).drop_duplicates(subset=['Title', 'Name'], keep='first')
    # get occurances on monsters throughout series
    monster_occurance_data = monster_occurance_data.groupby(['Name', 'Type'])['Title'].count().to_frame(
        name='Occurance').reset_index().sort_values(by=['Type', 'Occurance'], ascending='False')
    # get max occurances
    max_occ_monsters = monster_occurance_data.groupby('Type')['Occurance'].max().reset_index()
    # join Max occurances
    max_occ_monsters = pd.merge(monster_occurance_data, max_occ_monsters, on='Type', suffixes=('', '_max'))
    max_occ_monsters = max_occ_monsters[max_occ_monsters['Occurance'] == max_occ_monsters['Occurance_max']]
    return max_occ_monsters.sort_values(by=['Occurance', 'Type'], ascending=False).reset_index(drop=True)[['Name', 'Type', 'Occurance']]


def get_director_df(mh_data):
    director_data = mh_data.sort_values(by=['Date Released']).drop_duplicates(subset=['Name'], keep='first')

    fujioka_titles = director_data[director_data['Director'] == 'Kaname Fujioka'][
        ['Title', 'Date Released', 'Director']].drop_duplicates(subset=['Title'],keep='first')
    ichinose_titles = director_data[director_data['Director'] == 'Yasunori Ichinose'][
        ['Title', 'Date Released', 'Director']].drop_duplicates(subset=['Title'],keep='first')
    tokuda_titles = director_data[director_data['Director'] == 'Yuya Tokuda'][
        ['Title', 'Date Released', 'Director']].drop_duplicates(subset=['Title'],keep='first')

    fujioka_monsters = director_data[director_data['Director'] == 'Kaname Fujioka'][['Name', 'Title']]
    ichinose_monsters = director_data[director_data['Director'] == 'Yasunori Ichinose'][['Name', 'Title']]
    tokuda_monsters = director_data[director_data['Director'] == 'Yuya Tokuda'][['Name', 'Title']]

    # fujioka
    fujioka_titles["Total Monsters"] = fujioka_titles['Title'].apply(lambda title:
                                                                     mh_data[mh_data['Title'] == title][
                                                                         'Name'].drop_duplicates().count()
                                                                     )
    fujioka_titles["Director Monsters"] = fujioka_titles['Title'].apply(lambda title:
                                                                        mh_data[(mh_data['Title'] == title) & (
                                                                                    mh_data['Name'].isin(
                                                                                        fujioka_monsters[
                                                                                            'Name']) == True)][
                                                                            'Name'].drop_duplicates().count()
                                                                        )
    # ichinose
    ichinose_titles["Total Monsters"] = ichinose_titles['Title'].apply(lambda title:
                                                                       mh_data[mh_data['Title'] == title][
                                                                           'Name'].drop_duplicates().count()
                                                                       )
    ichinose_titles["Director Monsters"] = ichinose_titles['Title'].apply(lambda title:
                                                                          mh_data[(mh_data['Title'] == title) & (
                                                                                      mh_data['Name'].isin(
                                                                                          ichinose_monsters[
                                                                                              'Name']) == True)][
                                                                              'Name'].drop_duplicates().count()
                                                                          )
    # tokuda
    tokuda_titles["Total Monsters"] = tokuda_titles['Title'].apply(lambda title:
                                                                   mh_data[mh_data['Title'] == title][
                                                                       'Name'].drop_duplicates().count()
                                                                   )
    tokuda_titles["Director Monsters"] = tokuda_titles['Title'].apply(lambda title:
                                                                      mh_data[(mh_data['Title'] == title) & (
                                                                                  mh_data['Name'].isin(tokuda_monsters[
                                                                                                           'Name']) == True)][
                                                                          'Name'].drop_duplicates().count()
                                                                      )
    concat_director = pd.concat([fujioka_titles, ichinose_titles, tokuda_titles]).sort_values(by='Date Released')
    concat_director['Director Monster Ratio'] = concat_director['Director Monsters'] / concat_director['Total Monsters']
    return concat_director, pd.DataFrame([["Kaname Fujioka", fujioka_titles['Title'].count(), fujioka_monsters['Name'].count()],
                  ["Yasunori Ichinose", ichinose_titles['Title'].count(), ichinose_monsters['Name'].count()],
                  ["Yuya Tokuda", tokuda_titles['Title'].count(), tokuda_monsters['Name'].count()]],
                 columns=['Director', 'Titles', 'Total Director Monsters'])

def get_types_df(mh_data):
    monster_type_data = mh_data.drop_duplicates(subset=['Name']).groupby('Type').count()['Name'].to_frame(
        'Count').reset_index().sort_values(by='Count', ascending=False)
    monster_type_intro_date = mh_data.sort_values(by='Date Released').drop_duplicates(subset=['Type'],
                                                                                           keep='first')
    return monster_type_data, monster_type_intro_date[['Type', 'Title', 'Date Released']].reset_index(drop=True)