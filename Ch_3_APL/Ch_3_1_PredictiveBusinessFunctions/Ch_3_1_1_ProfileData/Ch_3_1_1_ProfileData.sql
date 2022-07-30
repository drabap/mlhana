/*
 * Kapitel 3.1.1 - Statistiken mit Profile Data berechnen
 *               - Aufruf Predictive Business Service --> Profile Data
 *               - Datenmenge: ML_DATA.CHURN
 *               - Ablage der Ergebnisse in Schema ML_APL
 */


/*
 * Listing: Vorbereiten der Eingabeparameter für PROFILE_DATA 
 *  
 */ 

SET SESSION 'APL_CACHE_SCHEMA' = 'APL_CACHE';
SET SCHEMA ML_APL;

-- Bei zweitem Aufruf: Erst Tabellen löschen
-- DROP TABLE ML_APL.FUNC_HEADER;
-- DROP TABLE ML_APL.PROFILE_DATA_CONFIG;
-- DROP TABLE VARIABLE_ROLES;
-- DROP TABLE VARIABLE_DESC;

CREATE TABLE FUNC_HEADER LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";
INSERT INTO FUNC_HEADER VALUES ('Oid', '#42');
INSERT INTO FUNC_HEADER VALUES ('LogLevel', '8');

CREATE TABLE PROFILE_DATA_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_EXTENDED";
CREATE TABLE VARIABLE_ROLES LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_ROLES_WITH_COMPOSITES_OID";
CREATE TABLE VARIABLE_DESC LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_DESC_OID";

/*
 * Listing: Aufruf PROFILE_DATA in anonymen Block
 * - Ausgabe der Rückgabeparameter
 * - Speichert Indicators in ML_APL.INDICATORS für spätere Verwendung
 */

DO BEGIN     
   

lt_header           = SELECT * FROM FUNC_HEADER;             
lt_config           = SELECT * FROM PROFILE_DATA_CONFIG;  
lt_variable_desc    = SELECT * FROM VARIABLE_DESC;
lt_variable_roles    = SELECT * FROM VARIABLE_ROLES;

"SAP_PA_APL"."sap.pa.apl.base::PROFILE_DATA"(:lt_header,
    :lt_config,
    :lt_variable_desc, 
    :lt_variable_roles, 
    'ML_DATA',
    'CHURN', 
    out_operation_log,
    out_summary, 
    out_indicators,
    out_variable_desc);

-- Bei zweitem Aufruf => Tabelle löschen
-- DROP TABLE ML_APL.INDICATORS;
CREATE TABLE ML_APL.INDICATORS AS 
    ( SELECT * FROM :out_indicators ); 
    
-- Ergebnisse ausgeben
SELECT * FROM :out_operation_log;
SELECT * FROM :out_summary;
SELECT * FROM :out_indicators;
SELECT * FROM :out_variable_desc;
    
END;