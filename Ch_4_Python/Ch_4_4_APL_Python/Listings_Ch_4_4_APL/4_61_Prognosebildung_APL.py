# Prognosebildung mit APL
l_df_result = g_gradboost_c.predict( g_df_test )

l_df_result.collect()
