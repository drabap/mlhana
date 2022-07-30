# Entfernen von Spalten mit dem Deselect-Befehl
l_df_reduced = g_df_source.deselect(['ROWNUMBER','SURNAME'])
l_df_reduced.collect()
