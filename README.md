# ArcGIS Metadata Geoprocessing Scripts

Collection of ArcGIS 10.3 Metadata python geoprocessing scripts. For more information, please see the tool descriptions in ArcGIS toolbox.

These scripts only work with ArcGIS Metadata Style. Convert FGDC or old ESRIISO format to ArcGIS sytle. 

## Scripts
- [ArcGIS_metadata_tags.py](scripts/ArcGIS_metadata_tags.py): Collection of ArcGIS Style xml element tags.
- [arcgisgp_metadata_add_contact.py](scripts/arcgisgp_metadata_add_contact.py): Add a full contact (batch script).
- [arcgisgp_metadata_add_prcstep_batch.py](scripts/arcgisgp_metadata_add_prcstep_batch.py): Add a process step in Lineage section (batch scritp).
- [arcgisgp_metadata_date_update.py](scripts/arcgisgp_metadata_date_update.py): Update (batch scritp) dates (creation, publication, revised, and temporal extent instant date).
- [arcgisgp_metadata_exactcopy_multiple.py](scripts/arcgisgp_metadata_exactcopy_multiple.py): Export an exact copy of metadata (batch scritp).

- [arcgisgp_metadata_fields_update.py](scripts/arcgisgp_metadata_fields_update.py): Import Entity Attribute from the source metadata if matching fields exist.

- [arcgisgp_metadata_simple_updater.py](scripts/arcgisgp_metadata_simple_updater.py): Simple metadata updater. Utilize xml template (Metadata_Template.xml).
    - title
    - keywords
    - summary
    - description
    - credit
    - default contact info (from template)
    - use limitation (from template)
    - delete data quality and lineage
    - delete lanagage and country code
    - update revised date as today
    - thumbnail
    
- [Metadata_Template.xml](scripts/Metadata_Template.xml): XML Metadata template for default contact info and use limitation. Update(revise) the template with your org info.

- [sl_meta_functs.py](scripts/sl_meta_functs.py): xml edit helper.