import matplotlib.pyplot as plt
import numpy as np

def make_amt_monsters_figure(amt_monsters_df):
    labels = amt_monsters_df['Title'].apply(lambda x: x + " " * 2)
    amt_monsters = amt_monsters_df['Total Monsters']
    large_monters = amt_monsters_df['Large Monsters']
    small_monsters = amt_monsters_df['Small Monsters']
    total_new_monsters = amt_monsters_df['New Monsters']
    new_large_monsters = amt_monsters_df['New Large Monsters']
    new_small_monsters = amt_monsters_df['New Small Monsters']
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    ax.grid(axis='x', zorder=0)
    width = 0.25
    rects1 = np.arange(len(labels))
    rects2 = [x + width for x in rects1]
    rects3 = [x + width for x in rects2]
    rects4 = rects1
    rects5 = rects2
    rects6 = rects3
    ax.barh(rects1, amt_monsters, height=width, edgecolor='white', label='Total Monsters', color='#cb6a63', zorder=2)
    ax.barh(rects2, large_monters, height=width, edgecolor='white', label='Large Monsters', color='#736aab', zorder=2)
    ax.barh(rects3, small_monsters, height=width, edgecolor='white', label='Small Monsters', color='#d9b66f', zorder=2)
    ax.barh(rects4, total_new_monsters, height=width, edgecolor='white', label='New Monsters', color='#ce9f97',
            hatch='/', zorder=2)
    ax.barh(rects5, new_large_monsters, height=width, edgecolor='white', label='New Large Monsters', color='#adaabf',
            hatch='/', zorder=2)
    ax.barh(rects6, new_small_monsters, height=width, edgecolor='white', label='New Small Monsters', color='#d2bc96',
            hatch='/', zorder=2)
    ax.set_xlabel("Number of Monsters", fontsize='15', color='#423e35')
    ax.set_yticks(rects1)
    ax.set_yticklabels(labels, fontsize='15', color='#423e35')
    ax.legend(fontsize='12')
    ax.invert_yaxis()
    ax.set_title('Amount of Monsters in Mainline Series', color='#423e35', fontsize='20')
    ax.set_facecolor('#fcf3ea')
    fig.set_facecolor('#fcf3ea')
    fig.set_edgecolor(color='#98805c')
    fig.patch.set_linewidth('1')
    fig.savefig('Figures/amt_monsters.png',
                facecolor=fig.get_facecolor(),
                edgecolor=fig.get_edgecolor(),
                bbox_inches="tight")

def make_base_ultimate_figure(base_ultimate):
    labels = ['Monster Hunter \nvs          \n Monster Hunter G',
              'Monster Hunter Portable 2nd \nvs          \n Monster Hunter Portable 2nd G',
              'Monster Hunter 3 \nvs          \n Monster Hunter 3 G',
              'Monster Hunter 4 \nvs          \n Monster Hunter 4 G',
              'Monster Hunter X \nvs          \n Monster Hunter XX',
              'Monster Hunter: World \nvs          \n Monster Hunter World: Iceborne']
    monsters_diff = base_ultimate['Monster Difference']
    var_monster_diff = base_ultimate['Variant Monster Difference']
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    ax.grid(axis='x', zorder=0)
    width = 0.25
    rects1 = np.arange(len(labels))
    rects2 = [x + width for x in rects1]
    ax.barh(rects1, monsters_diff, height=width, edgecolor='white', label='Total Monsters', color='#cb6a63', hatch='',
            zorder=2)
    ax.barh(rects2, var_monster_diff, height=width, edgecolor='white', label='Total Monsters', color='#d2bc96',
            hatch='', zorder=2)
    ax.set_yticks(rects1)
    ax.set_yticklabels(labels, fontsize='17', color='#423e35')
    ax.invert_yaxis()
    ax.set_title('Base Game Vs Ultimate Expansion', color='#423e35', fontsize='20')
    ax.set_xlabel('Amount of Monsters', fontsize='15', color='#423e35')
    ax.set_facecolor('#fcf3ea')
    ax.legend(['Monster Difference Between Games', 'Variant Monsters Added in Ultimate Expansion'])
    fig.set_facecolor('#fcf3ea')
    fig.set_edgecolor(color='#98805c')
    fig.patch.set_linewidth('1')
    fig.savefig('Figures/base_vs_ultimate.png',
                facecolor=fig.get_facecolor(),
                edgecolor=fig.get_edgecolor(),
                bbox_inches="tight")

def make_director_figure(director_title_data):
    labels = director_title_data['Director'].unique()
    fujioka_data = director_title_data[director_title_data['Director'] == 'Kaname Fujioka']
    ichinose_data = director_title_data[director_title_data['Director'] == 'Yasunori Ichinose']
    tokuda_data = director_title_data[director_title_data['Director'] == 'Yuya Tokuda']

    fujioka_titles = fujioka_data['Title'].to_list()
    ichinose_titles = ichinose_data['Title'].to_list()
    tokuda_titles = tokuda_data['Title'].to_list()

    fujioka_tm = fujioka_data['Total Monsters'].to_list()
    fujioka_dm = fujioka_data['Director Monsters'].to_list()

    ichinose_tm = ichinose_data['Total Monsters'].to_list()
    ichinose_dm = ichinose_data['Director Monsters'].to_list()

    tokuda_tm = tokuda_data['Total Monsters'].to_list()
    tokuda_dm = tokuda_data['Director Monsters'].to_list()

    xlim = (0, 140)
    ylim = (-1, 7)
    fig, (ax0, ax1, ax2) = plt.subplots(3, figsize=(10, 10), dpi=80)
    plt.setp(ax0, xlim=xlim, ylim=ylim)
    plt.setp(ax1, xlim=xlim, ylim=ylim)
    plt.setp(ax2, xlim=xlim, ylim=ylim)
    width = 0.25
    rects1 = np.arange(len(fujioka_titles))
    rects2 = [x + width for x in rects1]
    ax0.barh(rects1, fujioka_tm, height=width, edgecolor='white', label='Total Monsters', color='#cb6a63', zorder=2)
    ax0.barh(rects2, fujioka_dm, height=width, edgecolor='white', label='Director Monsters', color='#736aab', zorder=2)
    # ax0.set_xlabel("Number of Monsters", fontsize='12', color='#423e35')
    ax0.set_yticks(rects1)
    ax0.set_yticklabels(fujioka_titles, fontsize='15', color='#423e35')
    # ax0.legend(fontsize='12')
    ax0.invert_yaxis()
    ax0.set_title('Kaname Fujioka Monsters', color='#423e35', fontsize='20')
    ax0.set_facecolor('#fcf3ea')
    ax0.grid(axis='x', zorder=0)

    rects1 = np.arange(len(ichinose_titles))
    rects2 = [x + width for x in rects1]
    ax1.barh(rects1, ichinose_tm, height=width, edgecolor='white', label='Total Monsters', color='#cb6a63', zorder=2)
    ax1.barh(rects2, ichinose_dm, height=width, edgecolor='white', label='Director Monsters', color='#736aab', zorder=2)
    # ax1.set_xlabel("Number of Monsters", fontsize='12', color='#423e35')
    ax1.set_yticks(rects1)
    ax1.set_yticklabels(ichinose_titles, fontsize='15', color='#423e35')
    # ax1.legend(fontsize='12')
    ax1.invert_yaxis()
    ax1.set_title('Yasunori Ichinose Monsters', color='#423e35', fontsize='20')
    ax1.set_facecolor('#fcf3ea')
    ax1.grid(axis='x', zorder=0)

    rects1 = np.arange(len(tokuda_titles))
    rects2 = [x + width for x in rects1]
    ax2.barh(rects1, tokuda_tm, height=width, edgecolor='white', label='Total Monsters', color='#cb6a63', zorder=2)
    ax2.barh(rects2, tokuda_dm, height=width, edgecolor='white', label='Director Monsters', color='#736aab', zorder=2)
    # ax2.set_xlabel("Number of Monsters", fontsize='12', color='#423e35')
    ax2.set_yticks(rects1)
    ax2.set_yticklabels(tokuda_titles, fontsize='15', color='#423e35')
    ax2.legend(fontsize='15', loc=3)
    ax2.invert_yaxis()
    ax2.set_title('Yuya Tokuda Monsters', color='#423e35', fontsize='20')
    ax2.set_facecolor('#fcf3ea')
    ax2.grid(axis='x', zorder=0)

    fig.set_facecolor('#fcf3ea')
    fig.set_edgecolor(color='#98805c')
    fig.patch.set_linewidth('1')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle('Directors Monster Throughout the Series',fontsize='22',color='#423e35')
    fig.supxlabel("Number of Monsters", fontsize='15', color='#423e35')
    fig.savefig('Figures/directors_monsters.png',
                facecolor=fig.get_facecolor(),
                edgecolor=fig.get_edgecolor(),
                bbox_inches="tight")

def make_type_figure(monster_type_data):
    labels = monster_type_data['Type']
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    ax.grid(axis='x', zorder=0)
    width = 0.25
    rects1 = np.arange(len(labels))
    ax.barh(rects1, monster_type_data['Count'], height=width, edgecolor='white', label='Total Monsters',
            color='#cb6a63', zorder=2)
    ax.set_yticks(rects1)
    ax.set_yticklabels(labels, fontsize='15', color='#423e35')
    ax.invert_yaxis()
    ax.set_title('Distribution of Monsters Types \nin Mainline Series', color='#423e35', fontsize='20')
    ax.set_xlabel('Number of Monsters', fontsize='15',color='#423e35')
    ax.set_facecolor('#fcf3ea')
    fig.set_facecolor('#fcf3ea')
    fig.set_edgecolor(color='#98805c')
    fig.patch.set_linewidth('1')
    fig.savefig('Figures/types_monsters.png',
                facecolor=fig.get_facecolor(),
                edgecolor=fig.get_edgecolor(),
                bbox_inches="tight")