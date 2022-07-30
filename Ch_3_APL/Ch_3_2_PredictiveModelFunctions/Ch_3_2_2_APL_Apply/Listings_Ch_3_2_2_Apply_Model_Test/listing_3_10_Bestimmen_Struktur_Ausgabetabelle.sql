DO BEGIN

lt_apply_func_header = SELECT * FROM APPLY_FUNC_HEADER;
lt_model_train = SELECT * FROM MODEL_TRAIN_BIN;
lt_apply_config = SELECT * FROM APPLY_CONFIG;

CALL "SAP_PA_APL"."sap.pa.apl.base::GET_TABLE_TYPE_FOR_APPLY"(
    :lt_apply_func_header,
    :lt_model_train,
    :lt_apply_config,
    'ML_APL','CHURN_TEST',
    lt_output_table,
    lt_log);

SELECT * FROM :lt_output_table;

END;
