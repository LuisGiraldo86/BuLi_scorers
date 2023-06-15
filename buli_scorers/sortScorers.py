"""
Author: LuisG, luisggon@protonmail.com
Created: January 25, 2023
Updated, June, 2023

Script to sort the goal scorers according to the total goals scored and the total of penalty kicks scored
"""

# imports
import pandas as pd

# load data
df_scorers = pd.read_csv('data/scorer_table.csv')
df_scorers

df_scorers['Platz'] = df_scorers['Platz'].apply(lambda x: int(x))

# ===================================================
#                AUXILIARY FUNCTIONS
# ===================================================

def scorer_platz(data: pd.DataFrame)->pd.DataFrame:

    data_ordered = data.sort_values(['Tore', 'Elfmeter'], ascending=[False, False])
    platz = 1

    for k in range(len(data)):

        data_ordered.iloc[k,0] = platz
        if k == len(data)-1: break
        if data_ordered.iloc[k, 2] > data_ordered.iloc[k+1, 2]: platz +=1

    return data_ordered

# ========================================================================

# sort the scorer by goals scored
df_scorers = scorer_platz(df_scorers)
df_scorers.to_csv('data/scorer_table_sorted.csv', index=False)