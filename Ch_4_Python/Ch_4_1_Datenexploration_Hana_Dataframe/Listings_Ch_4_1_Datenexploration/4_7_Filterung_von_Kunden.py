# Filterung von Kunden
l_df_filter = g_df_source.filter("""
(Geography = 'France' AND NUMOFPRODUCTS = 1) 
OR 
(Geography = 'Germany' AND ( NUMOFPRODUCTS IN (3,4) ))""")
l_df_filter.collect()

# Validierung: 
l_df_filter.distinct(['GEOGRAPHY','NUMOFPRODUCTS']).collect()
