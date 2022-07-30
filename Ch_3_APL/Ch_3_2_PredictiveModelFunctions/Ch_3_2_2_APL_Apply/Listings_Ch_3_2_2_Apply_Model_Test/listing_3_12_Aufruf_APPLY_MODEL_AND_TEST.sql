-- Ab zweiter Ausführung: Tabelle löschen
-- DROP TABLE MODEL_TEST_BIN;
-- DROP TABLE APPLY_TEST_INDICATOR;
CREATE COLUMN TABLE APPLY_TEST_INDICATOR LIKE 
 "SAP_PA_APL"."sap.pa.apl.base::BASE.T.INDICATORS";

DO BEGIN

lt_apply_func_header = SELECT * FROM APPLY_FUNC_HEADER;
lt_model_train = SELECT * FROM MODEL_TRAIN_BIN;
lt_apply_config = SELECT * FROM APPLY_CONFIG;

DELETE FROM CHURN_APPLY;

CALL "SAP_PA_APL"."sap.pa.apl.base::APPLY_MODEL_AND_TEST"(
    :lt_apply_func_header,
    :lt_model_train,
    :lt_apply_config,
    'ML_APL','CHURN_TEST',
    'ML_APL','CHURN_APPLY',
    lt_model_out,
    lt_apply_log,
    lt_apply_test_indicator);

SELECT * FROM CHURN_APPLY;

INSERT INTO APPLY_TEST_INDICATOR
    ( SELECT * FROM :lt_apply_test_indicator );

CREATE TABLE MODEL_TEST_BIN AS
    ( SELECT * FROM :lt_model_out );

END;

