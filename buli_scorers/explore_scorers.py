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
There are 14 players without informantion on their FIFA eligibility
"""
mask_null = df_spielers['Nation'].isnull()
df_spielers[mask_null]

df_NoNation = df_spielers[mask_null]\
    .reset_index(drop=True)\
    .drop(columns=['Nation', 'Nationalelf'])

df_Nation = df_spielers[~mask_null].reset_index(drop=True)

# Recall that we had saved the elegibility information as a list of strings
# and Pandas loaded the column not as a list but as a string.
# Consequently, we must bring the list back otherwise we will have a problem when we 
# fill the missing data. 

df_Nation['Nation'] = df_Nation['Nation'].apply(literal_eval)

# Let us fill the missing data by hand

spieler_ID = df_NoNation['DFB_id'].to_list()

Nation_lst = [
    ['Deutschland', 'Kroatien'], ['Portugal', 'Guinea-Bissau'], ['Japan'], ['Ghana'], 
    ['Griechenland', 'Deutschland'], ['Norway'], ['Argentinien', 'Italien'], ['Norway'], ['Italien'], ['Senegal', 'Deutschland'], ['Tunesien'], ['Japan'], ['Schweiz', 'Kosovo'], ['Ungarn']
]

Nationalelf_lst = [
    'Deutschland', 'Portugal', 'Japan', 'Ghana', 'Griechenland', 'Norway', 'Argentina', 'Norway', 'Italien', 'Senegal', 'Tunesien', 'Japan', 'Schweiz', 'Ungarn'
]

df_toFill = pd.DataFrame({'DFB_id': spieler_ID, 'Nation': Nation_lst, 'Nationalelf': Nationalelf_lst})

df_NoNation = df_NoNation.merge(df_toFill, on='DFB_id')

df_spielers = pd.concat([df_NoNation, df_Nation], axis=0)\
    .sort_values(by='DFB_id').reset_index(drop=True)

df_spielers['num_choices'] = df_spielers['Nation']\
    .apply(lambda x: len(x))


mask_choices = df_spielers['num_choices']>1
df_elegibles = df_spielers[mask_choices] # in this case we want to keep the indices

df_elegibles.drop(columns=['DFB_id', 'link', 'choices'], inplace=True)

"""
with a careful analysis there are some incongruences with respect to Transfermarkt data

76	 | Roman Neustädter	| ['Deutschland', 'Russland']	                    | Russland
567	 | Raúl Bobadilla	| ['Argentinien', 'Paraguay']	                    | Paraguay
638	 | Pál Dardai	    | [''Ungarn']	                                    | Ungarn
3461 | Sébastien Haller	| ['Frankreich', "Elfenbeinküste (Côte d'Ivoire)"]	| Elfenbeinküste (Côte d'Ivoire)

"""

# fixing the errors
df_spielers.iloc[76, 4] = 'Russland'
df_spielers.iloc[567, 4] = 'Paraguay'
df_spielers.iloc[638, 4] = 'Ungarn'
df_spielers.iloc[638, 3] = ['Ungarn']
df_spielers.iloc[3461, 4] = "Elfenbeinküste (Côte d'Ivoire)"


df_spielers.to_csv('data/spielers_fixed.csv')