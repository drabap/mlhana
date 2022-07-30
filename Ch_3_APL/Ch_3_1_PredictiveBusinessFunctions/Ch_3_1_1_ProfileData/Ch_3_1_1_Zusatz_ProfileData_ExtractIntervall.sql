 /*
  * Kapitel 3.1.1
  * Zusatz: Aus Intervallangaben bei Indikator CategoryFrequency die Intervallgrenzen extrahieren und separat fortschreiben 
  *   => Aggregation in Data Preview möglich
  * Voraussetzung: Das Skript Ch_3_1_1_ProfileData.sql wurde ausgeführt. 
  *                Ergebnisse stehen in ML_APL.INDICATORS
  */

  DO BEGIN
	lt_freq = SELECT VARIABLE, 
                     CAST(VALUE as double) as value, 
                     CAST(DETAIL as nvarchar(45)) as detail_c from ML_APL.INDICATORS WHERE key = 'CategoryFrequency' 
                                                                                           and DETAIL LIKE  '%;%';


	-- Intervall-Klammern entfernen in Spalte detail_c
	lt_freq_2 = select variable, value,
						substr(detail_c,2,length(detail_c)-2) as detail_c from :lt_freq;
						
	-- Split bei ; => Einzelne Werte bekommen
	lt_freq_3 = select variable, value,
				substr_before(detail_c,';') as min_c, 
                substr_after(detail_c,';') as max_c from :lt_freq_2;						


	-- Cast nach double
	lt_freq_4 = select variable, value, 
                       cast(min_c as double) as min_d, 
                       cast(max_c as double) as max_d from :lt_freq_3;

    -- Bei zweitem Durchlauf: Tabelle INDI_BIN vorher löschen
    -- DROP TABLE  ML_APL.INDI_BIN;
	CREATE TABLE ML_APL.INDI_BIN AS ( select *,rank() over(partition by variable order by min_d) as rank from :lt_freq_4 );
END;