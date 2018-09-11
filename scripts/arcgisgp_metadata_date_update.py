from ArcGIS_metadata_tags import metaTag
import sl_meta_functs as meta
from sl_meta_functs import arcpy
from datetime import datetime
from os import path

def xmlout(inputPar):
    # set arcpy Describe object from input
    inputdesc = meta.arcpy.Describe(inputPar)
    # check input file is xml
    if (inputdesc.dataType == 'File') & (inputPar.lower().endswith('.xml')):
        return inputPar
    # check input data element is in the list
    elif inputdesc.dataType in ["FeatureClass", "Table", "Workspace", "ShapeFile", "FeatureDataset", "RasterDataset"]:
        return meta.xmlExport(inputPar)
    else:
        meta.printit("Please select an input from xml, shapefile, feature class, feature dataset, Table, or Workspace")
        quit()


def dateupdate(tag, inputdate):
    # check date tag exist, if not add elements
    tree.findaddmissingxmltagNoPrint(tag)
    # update publication date
    tree.findreplacexmltext(tag, inputdate)


def validate(date_text):
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        arcpy.AddMessage("\n *************************************************** ")
        arcpy.AddMessage(" *** Incorrect data format, should be YYYY-MM-DD *** ")
        arcpy.AddMessage(" *************************************************** \n")
        return False


# disable geoprocessing history logging
arcpy.SetLogHistory(False)

inputMetadatas = arcpy.GetParameterAsText(0)
credate = arcpy.GetParameterAsText(1)
pubdate = arcpy.GetParameterAsText(2)
revdate = arcpy.GetParameterAsText(3)
tmpositiondate = arcpy.GetParameterAsText(4)
inputmeta = inputMetadatas.split(";")

# loop datasets
for counter, inputFC in enumerate(inputmeta):
    inputFC = inputFC.replace("'", "")
    # set arcpy Describe object from input
    arcpy.AddMessage("\n## {} of {} : {}".format(counter+1, len(inputmeta), path.basename(inputFC)))
    # check input data element is in the list
    xmlfile = xmlout(inputFC)
    tree = meta.xmlMeta(xmlfile)
    tree_root = tree.getroot()

    # if date is "0000-00-00", script deletes the existing date from metadata
    if credate == "0000-00-00":
        tree.deletexmlTag2NoPrint(metaTag["createdate"])
        arcpy.AddMessage(" - Remove(Delete) Creation Date")
    elif credate != "":
        # ---- CREATION DATE ----#
        arcpy.AddMessage(" - Update Creation Date")
        if validate(credate):
            tempdate = credate + "T00:00:00"
            dateupdate(metaTag["createdate"], tempdate)

    if pubdate == "0000-00-00":
        tree.deletexmlTag2NoPrint(metaTag["pubDate"])
        arcpy.AddMessage(" - Remove(Delete) Publication Date")
    elif pubdate != "":
        # ---- PUBLICATION DATE ----#
        arcpy.AddMessage(" - Update Publication Date")
        if validate(pubdate):
            tempdate = pubdate + "T00:00:00"
            dateupdate(metaTag["pubDate"], tempdate)

    if revdate == "0000-00-00":
        tree.deletexmlTag2NoPrint(metaTag["revisedate"])
        arcpy.AddMessage(" - Remove(Delete) Revised Date")
    elif revdate != "":
        # ---- REVISED DATE ----#
        arcpy.AddMessage(" - Update Revised Date")
        if validate(revdate):
            tempdate = revdate + "T00:00:00"
            dateupdate(metaTag["revisedate"], tempdate)

    if tmpositiondate == "0000-00-00":
        tree.deletexmlTag2NoPrint(metaTag["tmPosition"])
        arcpy.AddMessage(" - Remove(Delete) Time Period Information Date")
    elif tmpositiondate != "":
        # ---- Time Period Information Date ----#
        arcpy.AddMessage(" - Update Time Period Information Date")
        if validate(tmpositiondate):
            tempdate = tmpositiondate + "T00:00:00"
            dateupdate(metaTag["tmPosition"], tmpositiondate)

    # write updates to xml file
    tree.writeXml(xmlfile)

    # set input data arcpy Describe object
    tardesc = meta.arcpy.Describe(inputFC)
    # check if input data type is in the list
    if tardesc.datatype in ["FeatureClass", "Table", "Workspace", "ShapeFile", "FeatureDataset", "RasterDataset"]:
        # import metadata back to feature class
        meta.arcpy.MetadataImporter_conversion(xmlfile, inputFC)
        # synchronize metadata
        meta.arcpy.SynchronizeMetadata_conversion(inputFC, "SELECTIVE")

arcpy.AddMessage(" ")