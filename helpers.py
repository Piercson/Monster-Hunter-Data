import re
import copy
# Input is a monster hunter df that contains ['Name']
# returns non variant/deviant/subspecies monsters
def filter_out_variants(df):
    monsters_df = df.reset_index()
    newIndex = monsters_df['Name'].str.len().sort_values(kind='heapsort').index
    monsters_df = monsters_df.reindex(newIndex)
    list_monsters = monsters_df['Name'].to_list()
    list_monsters_t = list_monsters
    list_monsters_t = copy.deepcopy(list_monsters)
    for monster in list_monsters:
        m = re.compile(monster)
        for monsterX in list_monsters:
            if m.search(monsterX):
                if monsterX != monster:
                    try:
                        list_monsters_t.remove(monsterX)
                    except:
                        pass
    list_nonVarient_monsters = list_monsters_t
    return monsters_df[monsters_df['Name'].isin(list_nonVarient_monsters) == True]['Name'].to_list()