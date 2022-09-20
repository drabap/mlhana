from hana_ml.text.tm import text_classification
res = text_classification(pred_data = df_input_test,
                          ref_data  = df_reference,
                          k_nearest_neighbours = 5,
                          thread_ratio = 0.5)

res.select('ID','RANK','CATEGORY_VALUE','SCORE').collect()