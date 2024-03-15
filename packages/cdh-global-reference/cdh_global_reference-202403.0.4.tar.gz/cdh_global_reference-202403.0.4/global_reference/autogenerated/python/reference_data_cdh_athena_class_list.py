# Databricks notebook source
from pyspark.sql.functions import col
from pathlib import Path
import os
dbutils_defined = 'dbutils' in locals() or 'dbutils' in globals()
if not dbutils_defined:
    from databricks.connect import DatabricksSession
    from databricks.sdk.core import Config

    databricks_profile = "reference_data_dev"
    databricks_profile = databricks_profile.upper()

    user_name = os.environ.get("USER") or os.environ.get("USERNAME")
    os.environ["USER_ID"] = user_name
    config = Config(profile=databricks_profile)
    spark = DatabricksSession.builder.sdkConfig(config).getOrCreate()
                
if dbutils_defined:

    dbutils.widgets.text('target_database', 'edav_dev_cdh.cdh_reference')


if dbutils_defined:

    dbutils.widgets.text('target_database', 'edav_dev_cdh.cdh_reference')


if dbutils_defined:

    dbutils.widgets.text('yyyy', '2024')


if dbutils_defined:

    dbutils.widgets.text('yyyy', '2024')


if dbutils_defined:

    dbutils.widgets.text('mm', '03')


if dbutils_defined:

    dbutils.widgets.text('mm', '03')


if dbutils_defined:

    dbutils.widgets.text('dd', 'NA')


if dbutils_defined:

    dbutils.widgets.text('dd', 'NA')


if dbutils_defined:

    dbutils.widgets.text('transmission_period', '03_2024')


if dbutils_defined:

    dbutils.widgets.text('transmission_period', '03_2024')

dict_parameters = {'target_database':'edav_dev_cdh.cdh_reference','yyyy':'2024','mm':'03','dd':'NA','transmission_period':'03_2024','environment':'dev'}

# COMMAND ----------
    
# COMMAND ----------
execute_results_flag = "skip_execute"
print('intentionally blank: update code to print debug')
df_results = spark.sql("""/*
Retrieves the 'class_key' column from the 'silver_athena_concept_class' view in the specified target database.

The 'class_key' is a standardized identifier for concept classes, which facilitates easier reference and use
in various analytical contexts. It is derived from concatenating 'vocabulary_id' and 'concept_class_id',
then applying a regular expression to replace non-word characters with underscores, and finally converting
to lowercase. This key uniquely represents each concept class within the view, supporting tasks such as
filtering, aggregation, and joining with other datasets on a consistent and meaningful basis.

Usage:
This query is intended for use in scenarios where a list of unique concept class identifiers is needed,
such as for filtering data in subsequent queries, performing data integration tasks, or supporting
data exploration and analysis efforts.

Before execution, replace {target_database} with the actual name of the target database where the view
'silver_athena_concept_class' resides. Ensure that you have read access to the target database and the
'silver_athena_concept_class' view.

Example:
SELECT class_key FROM my_database.silver_athena_concept_class""".format(**dict_parameters))
df_results.show()
listColumns=df_results.columns
if (df_results.count() > 0):
    if ("sql_statement" in listColumns):
        df_merge = spark.sql(df_results.first().sql_statement)
        df_merge.show()
    
# COMMAND ----------
execute_results_flag = "skip_execute"
print('intentionally blank: update code to print debug')
df_results = spark.sql("""Note: This example assumes that 'my_database' is replaced with the actual database name where the view is located.
*/

Select class_key from {target_database}.silver_athena_concept_class order by class_key""".format(**dict_parameters))
df_results.show()
listColumns=df_results.columns
if (df_results.count() > 0):
    if ("sql_statement" in listColumns):
        df_merge = spark.sql(df_results.first().sql_statement)
        df_merge.show()
    