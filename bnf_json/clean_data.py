import pandas as pd

df = pd.read_csv('tab_extraction_via_api.csv', sep='\t')

df['jour'] = pd.to_numeric(df['jour'], errors='coerce')
df['mois'] = pd.to_numeric(df['mois'], errors='coerce')

df_sorted = df.sort_values(by=['mois', 'jour'])

df_unique = df_sorted.drop_duplicates(subset=df.columns[1])

df_unique.to_csv('fichier_trie_sans_doublons.csv', index=False, sep='\t')

print(df_unique)
