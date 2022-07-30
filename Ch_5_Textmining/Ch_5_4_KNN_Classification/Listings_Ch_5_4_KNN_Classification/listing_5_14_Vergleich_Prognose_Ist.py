# Prognose der Kategorie => Kategorie mit RANK = 1 selektieren
res_predicted = res.filter('RANK = 1').select('ID','CATEGORY_VALUE','SCORE')

compare = res_predicted.alias('RES').join( df_input_knn.alias('INP'),
                                           condition = 'RES.ID = INP.ID',
                                           how = 'inner',
                                           select = [('RES.ID','KEY'),
                                                     ('INP.CATEGORY','CAT_ACTUAL'),
                                                     ('RES.CATEGORY_VALUE','CAT_PREDICTED'),
                                                     ('RES.SCORE','SCORE')
                                                     ])

compare.sort(['KEY','CAT_ACTUAL']).collect()