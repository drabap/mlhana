-- Bei zweitem Aufruf: Tabelle vorher löschen
-- DROP TABLE OPERATION_CONFIG;
CREATE TABLE OPERATION_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_DETAILED";

INSERT INTO OPERATION_CONFIG VALUES ('APL/ModelType','binary classification', null);
