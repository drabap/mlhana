# Selektion bestimmter Spalten
l_df_select = g_df_source.select(
    ['CUSTOMERID','CREDITSCORE','AGE','EXITED']
    )
l_df_select.collect()
