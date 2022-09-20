compare_agg = compare.agg(
    agg_list = [('count','KEY','col_count')] ,
    group_by = ['CAT_ACTUAL','CAT_PREDICTED']).sort(['CAT_ACTUAL','CAT_PREDICTED'])

compare_agg.collect()