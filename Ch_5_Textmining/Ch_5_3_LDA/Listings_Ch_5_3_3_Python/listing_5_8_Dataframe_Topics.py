from hana_ml import dataframe

connection = dataframe.ConnectionContext( KEY = 'DEV' )
df = connection.table('PAL_LDA_DOCUMENT_TOPIC_DIST',
    schema = 'ML_TEXT')

# Beispielausgabe
df.sort(['KEY','TOPIC_ID']).head(20).collect()
