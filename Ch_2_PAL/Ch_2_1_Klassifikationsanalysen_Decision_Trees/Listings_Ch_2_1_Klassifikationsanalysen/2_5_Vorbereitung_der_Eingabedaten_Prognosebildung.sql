-- Einfügen in anonymen Block aus Listing 2.2
-- Vorbereiten der Eingabedaten für die Prognosebildung
lt_input_prediction = SELECT CUSTOMERID,
    CREDITSCORE,
    GEOGRAPHY,
    GENDER,
    AGE,
    TENURE,
    BALANCE,
    NUMOFPRODUCTS,
    HASCRCARD,
    ISACTIVEMEMBER,
    ESTIMATEDSALARY FROM :lt_input_test;
