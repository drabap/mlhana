-- Ab zweitem Durchlauf: Tabellen vorher löschen
-- DROP TABLE MODEL_TRAIN_BIN;
-- DROP TABLE TRAIN_LOG;
-- DROP TABLE SUMMARY;
-- DROP TABLE INDICATORS_TRAIN;

DO BEGIN

lt_func_header = SELECT * FROM FUNC_HEADER;
lt_train_config = SELECT * FROM TRAIN_CONFIG;
lt_variable_desc = SELECT * FROM VARIABLE_DESC;
lt_variable_roles = SELECT * FROM VARIABLE_ROLES;

CALL "SAP_PA_APL"."sap.pa.apl.base::CREATE_MODEL_AND_TRAIN"(
    :lt_func_header,
    :lt_train_config,
    :lt_variable_desc,
    :lt_variable_roles,
    'ML_APL', 'CHURN_TRAIN',
    lt_model_train_bin,
    lt_train_log,
    lt_train_summary,
    lt_train_indicators);

SELECT * FROM :lt_model_train_bin;
SELECT * FROM :lt_train_log;
SELECT * FROM :lt_train_summary;
SELECT * FROM :lt_train_indicators;

CREATE TABLE MODEL_TRAIN_BIN LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.MODEL_BIN_OID";
INSERT INTO MODEL_TRAIN_BIN (SELECT * FROM :lt_model_train_bin);

CREATE TABLE TRAIN_LOG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_LOG";
INSERT INTO TRAIN_LOG (SELECT * FROM :lt_train_log);

CREATE TABLE SUMMARY LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.SUMMARY";
INSERT INTO SUMMARY (SELECT * FROM :lt_train_summary);

CREATE TABLE INDICATORS_TRAIN LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.INDICATORS";
INSERT INTO INDICATORS_TRAIN (SELECT * FROM :lt_train_indicators);

END;
