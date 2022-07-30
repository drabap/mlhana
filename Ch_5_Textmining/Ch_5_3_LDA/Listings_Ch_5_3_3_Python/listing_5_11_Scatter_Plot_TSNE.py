pd_res = df_tsne_res.collect()

pd_res.plot( kind = 'scatter',
    x = 'x',
    y = 'y',
    c = 'z',
    cmap = 'coolwarm' )