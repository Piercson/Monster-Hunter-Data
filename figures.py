import matplotlib.pyplot as plt
import numpy as np

def make_amt_monsters(amt_monsters_df):
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

def make_base_ultimate(base_ultimate):
    labels = ['Monster Hunter \nvs          \n Monster Hunter G',
              'Monster Hunter Freedom 2 \nvs          \n Monster Hunter Freedom Unite',
              'Monster Hunter 3 \nvs          \n Monster Hunter 3 Ultimate',
              'Monster Hunter 4 \nvs          \n Monster Hunter 4 G',
              'Monster Hunter X \nvs          \n Monster Hunter XX',
              'Monster Hunter: World \nvs          \n Monster Hunter World: Iceborne']
    monsters_diff = base_ultimate['monster_difference']
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    ax.grid(axis='x', zorder=0)
    width = 0.25
    rects1 = np.arange(len(labels))
    ax.barh(rects1, monsters_diff, height=width, edgecolor='white', label='Total Monsters', color='#809e6e')

    ax.set_yticks(rects1)
    ax.set_yticklabels(labels, fontsize='15', color='#423e35')
    ax.invert_yaxis()
    ax.set_title('Base Vs Ultimate', color='#423e35', fontsize='20')
    ax.set_xlabel('Difference of Monsters')
    ax.set_facecolor('#fcf3ea')
    fig.set_facecolor('#fcf3ea')
    fig.set_edgecolor(color='#98805c')
    fig.patch.set_linewidth('1')
    fig.savefig('Figures/base_vs_ultimate.png',
                facecolor=fig.get_facecolor(),
                edgecolor=fig.get_edgecolor(),
                bbox_inches="tight")