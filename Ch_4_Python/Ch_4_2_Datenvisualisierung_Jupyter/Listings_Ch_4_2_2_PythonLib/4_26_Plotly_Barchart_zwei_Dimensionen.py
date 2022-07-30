# Plotly: Barchart mit zwei Dimensionen
import plotly.express as px

# Aggregation: Anzahl Kündigenden nach Land und Anzahl Produkte
group_by_col_ext = ['GEOGRAPHY', 'NUMOFPRODUCTS', 'EXITED']

l_df_agg_ext = g_df_churn.agg(
    [('count',
    'CUSTOMERID',
    'COUNT_CUSTOMER')
    ],
    group_by = group_by_col_ext)

l_exp_label = """CASE EXITED WHEN 1 THEN 'EXITED'
 ELSE 'NOT EXITED' END"""

l_df_text_ext = l_df_agg_ext.select('*',
    (l_exp_label, 'EXIT_LABEL')
    )

# Umwandeln in Pandas-Dataframe
l_pd_df_ext = l_df_text_ext.sort(group_by_col_ext).collect()

# Zeichnen
fig = px.bar(l_pd_df_ext, 
    x = 'NUMOFPRODUCTS',
    y = 'COUNT_CUSTOMER', 
    color = 'EXIT_LABEL', 
    facet_row = 'GEOGRAPHY',
    # barmode = 'group',
    facet_row_spacing = 0.07,
    labels = {'COUNT_CUSTOMER' : 'Kunden',
              'EXIT_LABEL' : 'Kündigung'},
    color_discrete_sequence = px.colors.qualitative.D3 )

# Optional: "Compare data on hover" aktivieren
# fig.update_layout( hovermode = 'x' )

fig.show()
