/*
 Kapitel 5 - Textmining
 Abschnitt 5.3.2
 Aufruf Latent Dirichlet Allocation zur Themenextraktion
 - Input: NEWSCORP_PREP, Spalte TEXT_STEM -> Enthält die gefilterten Texte mit auf Stammform reduzierten Wörtern
*/

SET SCHEMA ML_TEXT;

-- Bei zweitem Aufruf: Parametertabellen und Ergebnistabellen löschen
DROP TABLE PAL_LDA_PARAMETER_TBL;

DROP TABLE PAL_LDA_DOCUMENT_TOPIC_DIST;
DROP TABLE PAL_LDA_TOPIC_TOP_WORDS;
DROP TABLE PAL_LDA_TOPIC_WORD_DISTRIBUTION_TBL;
DROP TABLE PAL_LDA_DICTIONARY_TBL;



CREATE COLUMN TABLE PAL_LDA_PARAMETER_TBL (
    "PARAM_NAME" VARCHAR(256), 
    "INT_VALUE" INTEGER,
    "DOUBLE_VALUE" DOUBLE,
    "STRING_VALUE" VARCHAR(1000));

-- Pflichtparameter
INSERT INTO PAL_LDA_PARAMETER_TBL VALUES (
    'TOPICS', 10, NULL, NULL);

-- Optionale Parameter
-- Alternativ zu MAX_TOP_WORDS: Angabe THRESHOLD_TOP_WORDS
INSERT INTO PAL_LDA_PARAMETER_TBL VALUES (
    'MAX_TOP_WORDS', 10, NULL, NULL);
-- INSERT INTO PAL_LDA_PARAMETER_TBL VALUES ('THRESHOLD_TOP_WORDS', NULL, 0.05, NULL);
-- Initialisierung Zufallsgenerator => vergleichbare Resultate
INSERT INTO PAL_LDA_PARAMETER_TBL VALUES (
    'SEED', 42, NULL, NULL);
INSERT INTO PAL_LDA_PARAMETER_TBL VALUES (
    'OUTPUT_WORD_ASSIGNMENT', 1, NULL, NULL);



DO BEGIN

lt_data = SELECT KEY, TEXT_STEM FROM ML_TEXT.NEWSCORP_PREP;

lt_param = SELECT * FROM PAL_LDA_PARAMETER_TBL;

CALL _SYS_AFL.PAL_LATENT_DIRICHLET_ALLOCATION ( 
    :lt_data,
    :lt_param,
    lt_document_topic_distribution,
    lt_word_topic_assignment,
    lt_topic_top_words,
    lt_topic_word_distribution,
    lt_dictionary,
    lt_statistics,
    lt_cv_parameter);

-- Ausgabe Themen und Schlagwörter pro Thema
SELECT * FROM :lt_topic_top_words;
-- Ausgabe Dokument zu Thema
SELECT * FROM :lt_document_topic_distribution;

-- Optional: Ausgabe Document Word Assignment => wird nicht in DB-Tabellen gespeichert
-- SELECT * FROM :lt_word_topic_assignment;


-- Einfügen der Ergebnisse in DB-Tabellen zur späteren Verwendung
CREATE TABLE PAL_LDA_DOCUMENT_TOPIC_DIST AS (SELECT * FROM :lt_document_topic_distribution);
CREATE TABLE PAL_LDA_TOPIC_TOP_WORDS AS (SELECT * FROM :lt_topic_top_words); 
                                        
CREATE TABLE PAL_LDA_TOPIC_WORD_DISTRIBUTION_TBL AS (SELECT * FROM :lt_topic_word_distribution);
CREATE TABLE PAL_LDA_DICTIONARY_TBL AS (SELECT * FROM :lt_dictionary);

END;
