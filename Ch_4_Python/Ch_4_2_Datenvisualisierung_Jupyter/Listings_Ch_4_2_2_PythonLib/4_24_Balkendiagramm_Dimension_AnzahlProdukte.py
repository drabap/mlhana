# Balkendiagramm mit Dimension Anzahl Produkte
import plotly.express as px

fig = px.bar(data_frame = l_pd_df,
    x = 'NUMOFPRODUCTS',
    y = 'COUNT_CUSTOMER',
    color = 'EXIT_LABEL',
    color_discrete_sequence = px.colors.qualitative.D3)
fig.show()
