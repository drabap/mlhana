# MALL_CUSTOMERS selektieren
from hana_ml import dataframe

conn = dataframe.ConnectionContext( KEY = 'DEV' )

g_df_mall_cust = conn.table(table = 'MALL_CUSTOMERS',
    schema = 'ML_DATA')
