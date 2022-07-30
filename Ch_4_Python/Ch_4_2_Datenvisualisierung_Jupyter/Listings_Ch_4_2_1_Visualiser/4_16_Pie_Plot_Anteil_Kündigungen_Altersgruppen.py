# Kreisdiagramm: Anteil Kündigungen in zwei Altersgruppen
df_age_below_50 = g_df_churn.filter('AGE <= 50')
df_age_above_50 = g_df_churn.filter('AGE > 50')

fig_churn_by_age = plt.figure(figsize = (18,6))
ax1 = fig_churn_by_age.add_subplot(121)
eda = EDAVisualizer(ax1)

ax1, pie_data = eda.pie_plot(data = df_age_below_50,
    column = 'EXITED',
    title ="Churn for Age <= 50")

ax2 = fig_churn_by_age.add_subplot(122)
eda2 = EDAVisualizer(ax2)
ax2, pie_data2 = eda2.pie_plot(data = df_age_above_50,
    column = 'EXITED',
    title ="Churn for Age >= 50")
