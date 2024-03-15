/*
Creates or replaces a dynamic view for concept categorization and hierarchy.

The view aggregates concept data from the source database's concept and concept_class tables,
along with their ancestors, to provide a structured view of concept metadata, categorization,
and hierarchical relationships based on a specific concept class. The view is dynamically
named based on a given concept list parameter and targets a specific database for view creation.

Parameters:
- {{target_database}}: The name of the database where the view will be created.  The ta
get database must be unity catalog enabled.
- {{concept_list_param}}: The specific concept class to filter and generate the view for.
  This parameter dynamically names the view and filters the data based on the class_key.
- {{source_database}}: The name of the database where the source tables will pull data.  The ta
source database must be unity catalog enabled.

Columns:
- meta_yyyy, meta_mm: Metadata fields indicating the year and month, respectively.
- class_code: The code representing the class of the concept.
- {{concept_list_param}}_key: The key for the concept, derived by trimming and modifying the concept_code.
- {{concept_list_param}}_code: The original code of the concept.
- {{concept_list_param}}: The name of the concept.
- {{concept_list_param}}_sort: A sorting index for the concepts, with a default of 0 if null.
- {{concept_list_param}}_parent: The parent concept's ID, indicating hierarchical relationships.
- parent_class_code: A duplicate of {{concept_list_param}}_parent for legacy support or additional hierarchical logic.
- {{concept_list_param}}_description: A static description for the concept; currently hard-coded as 'description'.
- {{concept_list_param}}_category: The domain ID of the concept, categorizing it within a broader domain.
- {{concept_list_param}}_category_sort: A static sorting index for the category, currently set to 1.
- {{concept_list_param}}_color: A static color code for the concept, currently hard-coded as 'hex'.

Joins:
- Joins concept_class (cc) and concept (c) tables based on class ID.
- Optionally joins the concept_ancestor (ca) table to provide ancestor concept IDs.

Filters:
- Only includes records where class_key matches the {{concept_list_param}}.

Ordering:
- Orders the output by year, month, ancestor concept ID, concept sort order, concept name,
  and parent class code to provide a consistent and logical ordering of concept records.

Usage:
This view is intended for dynamic querying of concept hierarchies and categorization within specific domains.
Replace {{target_database}}, {{source_database}}, and {{concept_list_param}} with actual values before execution.

Note: Ensure that the {{concept_list_param}} is appropriately sanitized and validated to prevent SQL injection
risks when using dynamic SQL generation techniques.
*/

Create
or replace view {{target_database}}.code_{{concept_list_param}} as
SELECT
  meta_yyyy,
  meta_mm,
  class_code as class_code,
  trim('{{concept_list_param}}') class_key,
  replace(concept_code, '_code','') {{concept_list_param}}_key,
  concept_code {{concept_list_param}}_code,
  concept_name  {{concept_list_param}},
  Try_Cast(coalesce(concept_sort,'0') as bigint) AS {{concept_list_param}}_sort,
  ancestor_concept_id  {{concept_list_param}}_parent,
  ancestor_concept_id AS  parent_class_code,
  'description'  {{concept_list_param}}_description,
  domain_id as {{concept_list_param}}_category,
  1 as {{concept_list_param}}_category_sort,
  'hex' as {{concept_list_param}}_color
from
  {{source_database}}.silver_athena_concept_class cc
  join {{source_database}}.bronze_athena_concept c on 
  c.concept_class_id = cc.concept_class_id
  left JOIN
  {{source_database}}.bronze_athena_concept_ancestor ca ON ca.ancestor_concept_id = c.concept_id
where
  class_key = '{{concept_list_param}}'
order by
  meta_yyyy,
  meta_mm,
  ancestor_concept_id,
  concept_sort,
  concept_name,
  parent_class_code;