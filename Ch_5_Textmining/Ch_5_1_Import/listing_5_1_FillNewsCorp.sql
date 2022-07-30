-- Einfügen der importierten Rohdaten aus NEWSCORP_RAW in die Tabelle NEWSCORP
-- Die Tabelle NEWSCORP hat einen Primärschlüssel KEY, der automatisch gefüllt wird
INSERT INTO NEWSCORP(CATEGORY,TEXT) SELECT * FROM NEWSCORP_RAW;

-- Zählen, ob alles richtig importiert wurde
SELECT CATEGORY, count(*) as COUNT_DOC
FROM ML_TEXT.NEWSCORP
GROUP BY CATEGORY