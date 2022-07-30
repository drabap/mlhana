# Berechnete Spalten
l_df_calc = g_df_source.select(['CUSTOMERID','SURNAME',
    'BALANCE','EXITED'])
# Text für EXITED
l_df_w_text = l_df_calc.select('*',
    ("""CASE EXITED WHEN 1 THEN 'EXITED' ELSE 'NOT EXITED' END""",
    'EXIT_LABEL'))

# Balance > 0 ?
l_df_w_balance = l_df_w_text.select('*',
    ('CASE WHEN BALANCE > 0 THEN 1 ELSE 0 END',
    'HAS_BALANCE')
    )

l_df_w_balance.collect()
