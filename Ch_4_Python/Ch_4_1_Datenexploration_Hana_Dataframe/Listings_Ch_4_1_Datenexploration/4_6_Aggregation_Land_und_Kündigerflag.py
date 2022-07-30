# Aggregation auf Ebene Land und Kündigungsflag
l_df_exited_per_country = g_df_source.agg([
    ('count','CUSTOMERID','COUNT_CUSTOMER')],
    group_by = ['GEOGRAPHY','EXITED'])
l_df_exited_per_country.sort(
    ['GEOGRAPHY','EXITED']).collect()
