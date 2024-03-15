# Databricks notebook source
catalog_name = 'edav_dev_cdh'
database_name = 'cdh_reference'

print(f"List tables in {catalog_name}.{database_name}")
tables = spark.catalog.listTables(f"{catalog_name}.{database_name}")

for table in tables:
    table_name = table.name
    full_table_name = f'{catalog_name}.{database_name}.{table_name}'
    print(full_table_name)
    if table.tableType == 'TABLE':
        sql_statement = f"DROP TABLE IF EXISTS {full_table_name}.{table_name}"
        print(sql_statement)
        spark.sql(sql_statement)

    spark.sql(f"VACUUM {full_table_name}")
