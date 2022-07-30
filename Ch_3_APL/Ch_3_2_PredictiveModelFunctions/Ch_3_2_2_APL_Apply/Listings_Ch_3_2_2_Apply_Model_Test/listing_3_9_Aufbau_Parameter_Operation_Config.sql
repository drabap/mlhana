-- Bei zweiter Ausführung: Tabelle löschen
-- DROP TABLE APPLY_CONFIG;

CREATE TABLE APPLY_CONFIG LIKE
"SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";

INSERT INTO APPLY_CONFIG VALUES 
('APL/ApplyExtraMode', 'Decision', null);
INSERT INTO APPLY_CONFIG VALUES ('APL/ApplyDecisionThreshold', '0.3', null);
