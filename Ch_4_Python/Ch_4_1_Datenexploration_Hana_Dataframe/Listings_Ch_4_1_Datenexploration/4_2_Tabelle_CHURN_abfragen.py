# Tabelle CHURN abfragen und auf 100 Zeilen reduzieren
g_df_source = connection.table( table = 'CHURN',
    schema = 'ML_DATA')
g_df_source.head(100).collect()
