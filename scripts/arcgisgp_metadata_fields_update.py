import os
import collections
import sl_meta_functs as meta
from sl_meta_functs import arcpy
from ArcGIS_metadata_tags import metaTag, dataDictionary

def xmlout(inputPar):
    # set arcpy Describe object from input
    inputdesc = meta.arcpy.Describe(inputPar)
    # check input file is xml
    if (inputdesc.dataType == 'File') & (inputPar.lower().endswith('.xml')):
        return inputPar
    # check input data element is in the list
    elif inputdesc.dataType in ["FeatureClass", "RasterDataset", "Workspace", "ShapeFile", "FeatureDataset", "Table", "TextFile"]:
        return xmlExport(inputPar)
    else:
        meta.printit("Please select correct data type to export Metadata")
        quit()


def xmlExport(fc):
    """
    Export metadata from the item and convert to a stand-alone xml file

    Parameters
    ----------
    fc: Data Element;Layer
        The item whose metadata will be converted or a stand-alone XML file that will be converted.
    Returns
    -------
    output_xml: File
        XML file
    """
    # arcgis install directory
    dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
    # exact copy xslt transformation
    xslt = dir + "Metadata/Stylesheets/gpTools/exact copy of.xslt"
    # set output directory
    out_dir = arcpy.env.scratchFolder
    # set arcpy workspace
    arcpy.env.workspace = out_dir
    # set workspace overwrite true
    arcpy.env.overwriteOutput = True
    #assemble output xml file name
    output_xml = os.path.join(out_dir, os.path.dirname(fc) + "." + os.path.basename(fc) + ".xml")
    #XSLT transforamtion
    arcpy.XSLTransform_conversion(fc, xslt, output_xml)
    return output_xml


def updateElemText(tag):
    # set source field attribute element
    sourceattrElem = source_attrElem_dict[attrlabel.text.lower()]
    # set source field attribute lable (name) element
    source_attr = sourceattrElem.find(tag)
    # if label elem is not none
    if source_attr is not None:
        if (tag == "attrdomv") & (attrElem.find(tag) is None):
            attrElem.append(source_attr)
        else:
            tempElem = attrElem.find(tag)
            if tempElem is None:
                childElem = meta.ET.Element(tag)
                attrElem.append(childElem)
            # set target field attribute desc
            attrElem.find(tag).text = source_attr.text


dataDictionary = collections.OrderedDict(dataDictionary)
source_metadata = arcpy.GetParameterAsText(0)
target_metadata = arcpy.GetParameterAsText(1)

skip_fields = ['objectid', 'shape', 'shape_length', 'shape_area']
sourceXML = xmlout(source_metadata)
targetXML = xmlout(target_metadata)
sourcetree = meta.xmlMeta(sourceXML)
targettree = meta.xmlMeta(targetXML)

source_attrElem = sourcetree.findxmltagAll(metaTag["eainfoattr"])
source_attrElem_dict = {elem.find(dataDictionary['fieldname']).text.lower():elem for elem in source_attrElem}

target_attrElem = targettree.findxmltagAll(metaTag["eainfoattr"])
target_attrElem_dict = {elem.find(dataDictionary['fieldname']).text:elem for elem in target_attrElem}

for attrElem in target_attrElem:
    # find target attrbiute element using field name
    attrlabel = attrElem.find(dataDictionary["fieldname"])
    # if field name is in skip list, also check similar name
    if len([attrlabel.text.lower() for fname in skip_fields if attrlabel.text.lower().find(fname) != -1]) == 0:
        if (attrlabel is not None) & (attrlabel.text.lower() in source_attrElem_dict):
            try:
                # field description
                updateElemText(dataDictionary["fielddesc"])
                # field description source
                updateElemText(dataDictionary["fielddescs"])
                # field value description (domain)
                updateElemText(dataDictionary["descvalue"])
            except:
                arcpy.AddMessage("Failed field name: {}".format(attrlabel.text))

targettree.writeXml(targetXML)
# import metadata back to feature class
meta.arcpy.MetadataImporter_conversion(targetXML, target_metadata)