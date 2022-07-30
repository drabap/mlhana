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
    -- SELECT * FROM :out_operation_log;
    -- SELECT * FROM :out_summary;
    SELECT * FROM :out_indicators;
    SELECT * FROM :out_influencers;
    -- SELECT * FROM :out_continuous_groups;
    -- SELECT * FROM :out_other_groups;
    
END;