# Dataset-Report erstellen
from hana_ml.visualizers.dataset_report import  DatasetReportBuilder

datasetReportBuilder = DatasetReportBuilder()
datasetReportBuilder.build( g_df_churn, key = 'CUSTOMERID')
datasetReportBuilder.generate_notebook_iframe_report()
