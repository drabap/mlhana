/*
 Erstellen der Tabelle NEWSCORP_PREP mit aufbereitetem Text:
	- Wörter, die nicht im Index vorkommen werden ausgefilert (z.B. Stopp-Wörter)
    - Wörter werden gemäß Textanalyseindex normalisiert
*/

SET SCHEMA ML_TEXT;

-- Evtl. vorhandene Tabelle löschen
DROP TABLE ML_TEXT.NEWSCORP_PREP;

CREATE COLUMN TABLE ML_TEXT.NEWSCORP_PREP ( 
KEY INT,
TEXT_ORG CLOB, -- Original-Token, Stopp-Wörter ausgefiltert
TEXT_STEM CLOB ); -- Wörter reduziert auf Stammform (was, being -> be)

DO

BEGIN

-- Einzelne Token pro Dokument aus Textanalyseindex (TA_NEWS_TEXT) selektieren 
-- und mit Textminingindex (TM_MATRIX_NEWS_TEXT) verknüpfen
-- Der Inner JOIN führt dazu, dass Tokens, die nicht in TM_MATRIX_NEWS_TEXT sind, entfernt werden
lt_tokens =  

SELECT
    TA.KEY, 
    TA.TA_COUNTER,
    TA.TA_TOKEN, 
    -- Anwenden der Normalisierung: Wenn TA_STEM gefüllt => wähle dies. Sonst TA_NORMALIZED oder das usprüngliche Wort (TA_TOKEN)
    COALESCE(TA_STEM, TA_NORMALIZED, TA_TOKEN) as TOKEN_REDUCED
FROM ML_TEXT."$TA_NEWS_TEXT" as TA 
INNER JOIN ML_TEXT."$TM_MATRIX_NEWS_TEXT" as M
ON TA.KEY = M.KEY -- Dokument
AND M.TM_TERM = TA.TA_TOKEN -- Token (Wort)
ORDER by TA.KEY, TA_COUNTER;
 
-- Ausgabe der reduzierten Tokens 
SELECT * FROM :lt_tokens;
 
lt_doc_preprocessed = 

SELECT KEY,
    STRING_AGG(TA_TOKEN, ' ') as TEXT_ORG,-- Originalwörter ohne Normalisierung
    STRING_AGG(TOKEN_REDUCED, ' ') as TEXT_STEM -- Wörter auf Stammform reduziert oder normalisiert
FROM :lt_tokens
GROUP BY KEY;
 
INSERT INTO NEWSCORP_PREP ( SELECT * FROM :lt_doc_preprocessed );
 
-- Ausgabe der finalen Tabelle
SELECT * FROM NEWSCORP_PREP; 
END;
