# Box-Plot für die Variable BALANCE
f = plt.figure(figsize=(18,6))

ax1 = f.add_subplot(121)
eda = EDAVisualizer(ax1)

df_bal = g_df_churn.filter("BALANCE > 0")
ax, bar_data = eda.box_plot(data= df_bal,
    column = 'BALANCE',
    # groupby = 'GEOGRAPHY',
    outliers = True )
