-- Ab zweitem Durchlauf: Tabelle vorher löschen
-- DROP TABLE TRAIN_CONFIG;
CREATE TABLE TRAIN_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";
INSERT INTO TRAIN_CONFIG VALUES ('APL/ModelType',
    'binary classification', null);
INSERT INTO TRAIN_CONFIG VALUES ('APL/IndicatorDataset',
    'Validation', null);
