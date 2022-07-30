-- Abfrage des Klassifikationsreport und Aufräumen

-- im anonymen Block aus Listing 2.2. hinter dem Code von Listing 2.8 einfügen
SELECT * FROM :lt_classification_report;

-- Clean up: Temporäre Tabelle für Parameter löschen
DROP TABLE #PAL_PARAMETER_TBL;