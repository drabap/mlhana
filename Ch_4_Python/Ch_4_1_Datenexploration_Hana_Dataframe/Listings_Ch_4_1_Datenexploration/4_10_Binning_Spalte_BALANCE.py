# Binning der Spalte BALANCE
l_df = g_df_source.select(['CUSTOMERID','BALANCE'])
# Binning uniform number
l_df_bin = l_df.bin(col = 'BALANCE',
    strategy = 'uniform_number',
    bins = 10,
    bin_column = 'BALANCE_BIN')

l_df_bin.collect()
