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