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
Creates or replaces a view named 'silver_athena_concept_class' within a specified target database.

This view transforms and consolidates concept class information from the 'bronze_athena_concept_class' table,
enhancing data readability and accessibility for downstream processing and analysis. The view introduces a
standardized 'class_key' for each concept class by concatenating 'vocabulary_id' and 'concept_class_id',
then applying a regular expression to replace non-word characters with underscores. This key facilitates
easier reference and use in various analytical contexts.

Columns:
- class_key: A unique identifier for each concept class, derived by concatenating the 'vocabulary_id' and
  'concept_class_id' fields, then replacing non-word characters with underscores. This key is presented in lowercase.
- concept_class_name: The name of the concept class as defined in the source table.
- class_code: A duplicate of 'class_key', provided for consistency and ease of use in queries.
- omop_table.concept_class_id: The original concept class ID from the source table.
- meta_yyyy, meta_mm: Metadata fields indicating the year and month of data processing. Hard-coded to 2024 and 03,
  respectively, to indicate the processing date or version of the view.
- concept_sort: A row number assigned based on the alphabetical ordering of 'vocabulary_id' and 'concept_class_name',
  used to establish a consistent sort order for the concept classes.

Source Data:
The view sources its data from 'edav_dev_cdh.cdh_reference.bronze_athena_concept_class' and applies a left join
with a subquery selecting distinct 'vocabulary_id' and 'concept_class_id' from 'edav_dev_cdh.cdh_reference.bronze_athena_concept'.
This join ensures that the view reflects a comprehensive and de-duplicated list of concept classes across different vocabularies.

Ordering:
Output records are ordered by 'vocabulary_id' and 'concept_class_name', ensuring a logical and consistent presentation
of concept class information.

Usage:
This view is intended for use in scenarios where standardized, easily queryable concept class information is needed.
It supports analytics, reporting, and data integration tasks by providing a clear, ordered, and enriched view of concept class data.

Note: Before execution, replace {target_database} with the actual name of the target database where the view will be created.
Ensure proper permissions are in place for creating or replacing views within the target database.
*/
Create or replace view {target_database}.silver_athena_concept_class As 
Select
    lower(REGEXP_REPLACE(
    CONCAT_WS(" | ", vocabulary_id, omop_table.concept_class_id),
    '\\W+',
    '_'
  )) class_key,
  concept_class_name,
  class_key class_code,
  omop_table.concept_class_id,
  2024 As meta_yyyy,
  03 as meta_mm,
  ROW_NUMBER() OVER (ORDER BY vocabulary_id, concept_class_name) concept_sort
from
  edav_dev_cdh.cdh_reference.bronze_athena_concept_class as omop_table
  left join (
    Select
      distinct vocabulary_id,
      concept_class_id
    from
     edav_dev_cdh.cdh_reference.bronze_athena_concept order by vocabulary_id, concept_class_id
  ) as omop_table_db_map on omop_table_db_map.concept_class_id = omop_table.concept_class_id
order by vocabulary_id, concept_class_name""".format(**dict_parameters))
df_results.show()
listColumns=df_results.columns
if (df_results.count() > 0):
    if ("sql_statement" in listColumns):
        df_merge = spark.sql(df_results.first().sql_statement)
        df_merge.show()
    