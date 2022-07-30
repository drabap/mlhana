/*
 * Kapitel 3.1.2 - Einflussfaktoren ermitteln
 *               - Aufruf Predictive Business Services --> Key Influencers
 *               - Grunddaten: ML_DATA.CHURN
 *               - Ablage der Ergebnisse in Schema ML_APL: INDICATORS und INFLUENCERS
 */


/*
 * Ausgelassen im Buch:
 * Vorbereiten der Eingabeparameter für KEY_INFLUENCERS
 *
 */

SET SESSION 'APL_CACHE_SCHEMA' = 'APL_CACHE';
SET SCHEMA ML_APL;

DROP TABLE FUNC_HEADER;
CREATE TABLE FUNC_HEADER LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.FUNCTION_HEADER";
INSERT INTO FUNC_HEADER VALUES ('Oid', '#42');
INSERT INTO FUNC_HEADER VALUES ('LogLevel', '8');

-- Listing: Modelltyp angeben bei KEY_INFLUENCERS
DROP TABLE OPERATION_CONFIG;
CREATE TABLE OPERATION_CONFIG LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.OPERATION_CONFIG_DETAILED";
INSERT INTO OPERATION_CONFIG VALUES ('APL/ModelType', 'binary classification', null);
-- Ende Listing: Modelltyp angeben bei KEY_INFLUENCERS

DROP TABLE VARIABLE_ROLES;
CREATE TABLE VARIABLE_ROLES LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_ROLES_WITH_COMPOSITES_OID";

DROP TABLE VARIABLE_DESC;
CREATE TABLE VARIABLE_DESC LIKE "SAP_PA_APL"."sap.pa.apl.base::BASE.T.VARIABLE_DESC_OID";
-- Tabelle leer lassen => APL ermittelt Vorschlag für Variablen


DO BEGIN     
   
    lt_header           = SELECT * FROM FUNC_HEADER;             
    lt_config           = SELECT * FROM OPERATION_CONFIG;  
    lt_variable_desc    = SELECT * FROM VARIABLE_DESC;
    lt_variable_roles    = SELECT * FROM VARIABLE_ROLES;

    "SAP_PA_APL"."sap.pa.apl.base::KEY_INFLUENCERS"(:lt_header, 
                                                    :lt_config,
                                                    :lt_variable_desc, 
                                                    :lt_variable_roles, 
                                                    'ML_DATA',
                                                    'CHURN', 
                                                 out_operation_log,
                                                 out_summary, 
                                                 out_indicators,
                                                 out_influencers,
                                                 out_continuous_groups, 
                                                 out_other_groups );

    -- Direkte Ausgabe der Ergebnisse
    --SELECT * FROM :out_operation_log;
    --SELECT * FROM :out_summary;
    SELECT * FROM :out_indicators;
    SELECT * FROM :out_influencers;
    --SELECT * FROM :out_continuous_groups;
    --SELECT * FROM :out_other_groups;
    
    /*
    * Ergänzung: Ergebnisse in Tabelle speichern
    */
    -- Bei zweitem Aufruf: Tabellen vorher löschen
    -- DROP TABLE "ML_APL"."INDICATORS";
    -- DROP TABLE "ML_APL"."INFLUENCERS";

    CREATE TABLE  "ML_APL"."INDICATORS" AS ( SELECT * FROM :out_indicators ); 
    
    
    
    CREATE TABLE "ML_APL"."INFLUENCERS" AS ( SELECT * FROM :out_influencers );
    
    
END;
