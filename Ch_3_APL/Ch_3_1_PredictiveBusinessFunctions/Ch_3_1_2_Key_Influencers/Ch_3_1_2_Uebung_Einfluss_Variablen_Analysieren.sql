/*
 * Listing zu Übungsbox: Einfluss der einzelnen Variablen analysieren
 *                       Extraktion der Indikatoren GroupFrequency, GroupTargetMean, GroupNormalProfit, GroupSignificance
*/

DO BEGIN
    
    -- Extraktion der Indikatoren und Cast der Spalte DETAIL
    lt_indicators_cast = SELECT variable, target,
                                                    case key 
                                                      when 'GroupFrequency' 
                                                      then
                                                            cast(value as double) 
                                                      else 0
                                                    end as GroupFrequency, 

                                                    case key 
                                                      when 'GroupTargetMean' 
                                                      then
                                                            cast(value as double) 
                                                      else 0
                                                    end as GroupTargetMean, 
                                                    
                                                    case key 
                                                      when 'GroupNormalProfit' 
                                                      then
                                                            cast(value as double) 
                                                      else 0
                                                    end as GroupNormalProfit, 
                                                    case key 
                                                      when 'GroupSignificance' 
                                                      then
                                                            cast(value as double) 
                                                      else 0
                                                    end as GroupSignificance, 
                                                    
                                                    cast(detail as char(255)) as detail 
    												FROM ML_APL.INDICATORS 
    												where key IN ( 'GroupTargetMean', 'GroupNormalProfit', 'GroupFrequency', 'GroupSignificance' ); 

   -- Aggregation auf den Spalten VARIABLE, TARGET, DETAIL    												
   lt_indicators_cast_agg = select variable, target, detail, sum(GroupFrequency) as GroupFrequency,
                                                             sum(GroupTargetMean) as GroupTargetMean,
                                                             sum(GroupNormalProfit) as GroupNormalProfit,
                                                             sum(GroupSignificance) as GroupSignificance
                                                             from :lt_indicators_cast 
                                                             group by variable, target, detail;
                                                                 												 
   -- Bei zweitem Aufruf: Tabelle INDICATORS_CAST löschen
   -- DROP TABLE ML_APL.INDICATORS_CAST;
   CREATE TABLE ML_APL.INDICATORS_CAST AS ( select * from :lt_indicators_cast_agg );
END;