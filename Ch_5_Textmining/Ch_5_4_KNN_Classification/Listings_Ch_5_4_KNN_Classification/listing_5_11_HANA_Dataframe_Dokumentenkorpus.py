# HANA-Dataframe für ML_TEXT.NEWSCORP

# Verbindung zur HANA
from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV')

df_newscorp = connection.table('NEWSCORP', 
                               schema = 'ML_TEXT')

# Umwandeln von CLOB nach NVARCHAR - Textmining-Paket unterstützt nur 5000 Zeichen
df_text = df_newscorp.cast('TEXT', 'NVARCHAR(5000)')

# Spalten umbenennen nach Vorgabe der Methode für Textklassifikation
df_input_knn = df_text.select(('KEY','ID'),
                              ('TEXT','CONTENT'),
                              'CATEGORY')
# Ausgabe der Daten zur Kontrolle
df_input_knn.collect()