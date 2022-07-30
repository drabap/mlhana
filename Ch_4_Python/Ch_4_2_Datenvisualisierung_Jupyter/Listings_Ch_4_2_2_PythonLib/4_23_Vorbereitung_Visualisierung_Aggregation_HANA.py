# Vorbereitung der Visualisierung: Aggregation in der HANA 
# Aggregation: Anzahl Kündigenden nach Anzahl Produkte
group_by_col = ['NUMOFPRODUCTS','EXITED']

l_df_agg = g_df_churn.agg(
    [('count',
    'CUSTOMERID',
    'COUNT_CUSTOMER')
    ],
    group_by = group_by_col)

l_exp_label = """CASE EXITED WHEN 1 THEN 'EXITED'
 ELSE 'NOT EXITED' END"""

l_df_w_text = l_df_agg.select(
    '*',
    (l_exp_label, 'EXIT_LABEL')
    )

# Umwandeln in Pandas Dataframe
l_pd_df = l_df_w_text.sort(group_by_col).collect()
# Zum Testen: Ausgeben des Pandas Dataframe
print(l_pd_df)
