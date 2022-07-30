# Verknüpfen von Prognoseergebnis und Testmenge
col_select = [('P.CUSTOMERID','CUSTOMERID'),
    ('P.SCORE','SCORE'),
    ('A.EXITED','EXITED')]

l_df_compare = g_df_predict_test.alias('P').join(
    other = g_df_test.alias('A'),
    condition = 'P.CUSTOMERID = A.CUSTOMERID',
    select = col_select)

l_df_compare = l_df_compare.cast('SCORE',
    'INT').rename_columns({'SCORE': 'PREDICTED'})

l_df_compare.head(20).collect()

