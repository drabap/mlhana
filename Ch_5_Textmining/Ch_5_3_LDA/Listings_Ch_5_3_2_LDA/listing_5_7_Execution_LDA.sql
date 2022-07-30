-- Vor zweiter Ausführung: Tabellen löschen
-- DROP TABLE PAL_LDA_DOCUMENT_TOPIC_DIST;
-- DROP TABLE PAL_LDA_TOPIC_TOP_WORDS;

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

-- Einfügen der Ergebnisse in DB-Tabellen zur späteren
-- Verwendung
CREATE TABLE PAL_LDA_DOCUMENT_TOPIC_DIST AS (SELECT * FROM :lt_document_topic_distribution);
CREATE TABLE PAL_LDA_TOPIC_TOP_WORDS AS (SELECT * FROM :lt_topic_top_words);
-- Ausgelassen: weitere Ergebnistabellen speichern
END;
