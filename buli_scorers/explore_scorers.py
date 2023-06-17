""" 
Author: LuisG, luisggon@protonmail.com
Created: June 17, 2023

Script to explorer the scrapped data from the 1.Bundesliga historical scorers.
"""

# imports
import pandas as pd
from ast import literal_eval

# load data
SCORERS_PATH = 'data/spielers.csv'
df_spielers = pd.read_csv(SCORERS_PATH)

df_spielers

# are there null values?
df_spielers.info()

"""
There are 14 players without informantion on its FIFA eligibility
"""
mask_null = df_spielers['Nation'].isnull()
df_spielers[mask_null]

df_spielerNoNation = df_spielers[mask_null]\
    .reset_index(drop=True)\
    .drop(columns=['Nation', 'Nationalelf'])

df_spielersNation = df_spielers[~mask_null].reset_index(drop=True)
# Pandas load the column with list as a string. We must bring back the list!
df_spielersNation['Nation'] = df_spielersNation['Nation'].apply(literal_eval)

"""
Let us fill the missing data by hand
"""

spieler_ID = df_spielerNoNation['DFB_id'].to_list()
Nation_lst = [['Deutschland', 'Kroatien'], ['Portugal', 'Guinea-Bissau'], ['Japan'], ['Ghana'], ['Griechenland', 'Deutschland'], ['Norway'], ['Argentinien', 'Italien'], ['Norway'], ['Italien'], ['Senegal', 'Deutschland'], ['Tunesien'], ['Japan'], ['Schweiz', 'Kosovo'], ['Ungarn']]

Nationalelf_lst = ['Deutschland', 'Portugal', 'Japan', 'Ghana', 'Griechenland', 'Norway', 'Argentina', 'Norway', 'Italien', 'Senegal', 'Tunesien', 'Japan', 'Schweiz', 'Ungarn']

df_toFill = pd.DataFrame({'DFB_id': spieler_ID, 'Nation': Nation_lst, 'Nationalelf': Nationalelf_lst})

df_spielerNoNation = df_spielerNoNation.merge(df_toFill, on='DFB_id')

df_spielers = pd.concat([df_spielerNoNation, df_spielersNation], axis=0)\
    .sort_values(by='DFB_id').reset_index(drop=True)

df_spielers['choices'] = df_spielers['Nation'].apply(
    lambda x: len(x)
)

pd.set_option('display.max_columns', None)
df_multi = df_spielers[df_spielers['choices']>1]

df_multi = df_multi.drop(columns=['DFB_id', 'link', 'choices'], inplace=False)

"""with a careful analysis there are some incongruences with respect to Transfermarkt data

76	 | Roman Neustädter	| ['Deutschland', 'Russland']	                    | Russland
567	 | Raúl Bobadilla	| ['Argentinien', 'Paraguay']	                    | Paraguay
638	 | Pál Dardai	    | [''Ungarn']	                                    | Ungarn
3461 | Sébastien Haller	| ['Frankreich', "Elfenbeinküste (Côte d'Ivoire)"]	| Elfenbeinküste (Côte d'Ivoire)

"""

df_spielers.iloc[76, 4] = 'Russland'
df_spielers.iloc[567, 4] = 'Paraguay'
df_spielers.iloc[638, 4] = 'Ungarn'
df_spielers.iloc[638, 3] = ['Ungarn']
df_spielers.iloc[3461, 4] = "Elfenbeinküste (Côte d'Ivoire)"


df_spielers.to_csv('data/spielers_fixed.csv')