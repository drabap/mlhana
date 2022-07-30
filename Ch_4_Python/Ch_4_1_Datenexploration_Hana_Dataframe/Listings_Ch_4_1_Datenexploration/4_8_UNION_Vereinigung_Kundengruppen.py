# UNION: Vereinigung zweier Kundengruppen
l_df_france_1 = g_df_source.filter("""
Geography = 'France' AND NUMOFPRODUCTS = 1
""")
l_df_germany_3_4 = g_df_source.filter("""
Geography = 'Germany' 
AND NUMOFPRODUCTS IN (3,4)""")

l_df_union = l_df_france_1.union(l_df_germany_3_4)
l_df_union.collect()
