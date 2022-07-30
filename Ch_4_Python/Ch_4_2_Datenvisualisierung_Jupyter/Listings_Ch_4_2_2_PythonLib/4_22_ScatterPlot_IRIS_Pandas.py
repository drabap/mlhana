# Scatter Plot von IRIS mit Pandas
pd_iris = g_df_iris.collect()

pd_iris['SPECIES'] = pd_iris['SPECIES'].astype('category')
pd_iris['SPECIES_CAT'] = pd_iris['SPECIES'].cat.codes

pd_iris.plot(kind = 'scatter',
    x = 'SEPAL_LENGTH',
    y = 'PETAL_WIDTH',
    c = 'SPECIES_CAT',
    cmap = 'coolwarm')
