# -*- coding: utf-8 -*-
import collections
import datetime
from ArcGIS_metadata_tags import metaTag, contacts, responsibleparty
import sl_meta_functs as meta
from sl_meta_functs import arcpy
contacts = collections.OrderedDict(contacts)
responsibleparty =  collections.OrderedDict(responsibleparty)

# populate contact information here
TEMPLATE = ([
    ("indName", ""),    #'John Doe'
    ("orgName", ""),    #'GIS Corp'
    ("posName", ""),    #'GIS Manager'
    ("contPhone", ""),  #'555-555-555'
    ("contFax", ""),    #'555-555-555'
    ("contAdddrs", ""), #'both', address type
    ("contAddrs", ""),  #'1 main street'
    ("contCity", ""),   #'Washington'
    ("contAdmAa", ""),  #'DC'
    ("contZip", ""),    #'20001'
    ("contCnty", ""),   #'US'
    ("contEmail", ""),  #'john,doe@metadata.org'
    ("contHours", ""),  #'8:30 am - 5 pm'
    ("contRole", ""),   #'007', point of contact
    ("contInstr", "")   #'During business hours only'
])

TEMPLATE = collections.OrderedDict(TEMPLATE)

def xmlout(inputPar):
    # check input file is xml
    if (inputdesc.dataType == 'File') & (inputPar.lower().endswith('.xml')):
        return inputPar
    # check input data element is in the list
    elif inputdesc.dataType in ["FeatureClass", "RasterDataset", "Workspace", "ShapeFile", "FeatureDataset", "Table", "TextFile"]:
        return meta.xmlExport(inputPar)
    else:
        meta.printit("Please select correct data type to export Metadata")
        quit()


def addChildElem(parentElem, chilxmltag):
    """Append child xml element"""
    child_element = meta.ET.Element(chilxmltag)
    parentElem.append(child_element)
    
    
def addChildElemandText(parentElem, chilxmltag, text = ""):
    """Append child xml element"""
    child_element = meta.ET.Element(chilxmltag)
    child_element.text = text
    parentElem.append(child_element)


def findaddmissingxmltag(parentElem, inputTag):
    """
    Search input tag (for example, "rpCntInfo/cntAddress/delPoint") from parent element
    and if any child tag is missing add the tag
    """
    tagList = inputTag.split("/")
    for j in range(len(tagList), 0, -1):
        tempTag = "/".join(tagList[0:j])

        # find and add missing child element/tag
        if parentElem.find(tempTag) is not None:
            temp_xml_tag = tempTag
            for k in range(j, len(tagList)):
                childTag = tagList[k]
                tempParElem = parentElem.find(temp_xml_tag)
                addChildElem(tempParElem, childTag)
                temp_xml_tag = "/".join(tagList[0:k + 1])
            break
        # add if input element/tag doesn't exist
        if j - 1 == 0:
            child_element = meta.ET.Element(tempTag)
            parentElem.append(child_element)
            temp_xml_tag = tempTag
            for l in range(1, len(tagList)):
                childTag = tagList[l]
                tempParElem = parentElem.find(temp_xml_tag)
                addChildElem(tempParElem, childTag)
                temp_xml_tag = "/".join(tagList[0:l + 1])


def validate(date_text):
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        arcpy.AddMessage("\n *************************************************** ")
        arcpy.AddMessage(" *** Incorrect data format, should be YYYY-MM-DD *** ")
        arcpy.AddMessage(" *************************************************** \n")
        return False


def dateupdate(tag, inputdate):
    # check date tag exist, if not add elements
    tree.findaddmissingxmltagNoPrint(tag)
    # update publication date
    tree.findreplacexmltext(tag, inputdate)


# input metadata (data elements)
src = arcpy.GetParameterAsText(0)
# process date
prcDate = arcpy.GetParameterAsText(1)
# process description
stepDesc = arcpy.GetParameterAsText(2)
# source list
src_metas = src.split(";")

# disable geoprocessing history logging
arcpy.SetLogHistory(False)

elemList = TEMPLATE.keys()

# create feature dataset list include root
for index, input_meta in enumerate(src_metas):
    input_meta = input_meta.replace("'", "")
    arcpy.AddMessage(" ")
    arcpy.AddMessage("{} of {}: {}".format(index + 1, len(src_metas), input_meta))
    # set arcpy Describe object from input
    inputdesc = arcpy.Describe(input_meta)

    arcpy.AddMessage("  # Process: Export Metadata")
    xml_file = xmlout(input_meta)

    # set xml tree element
    tree = meta.xmlMeta(xml_file)
    # root element
    root = tree.getroot()

    # ---- Process step contact ----#
    arcpy.AddMessage("  # Process: Add Process Steps")
    # input FC data quality element
    dq_elem = tree.findxmltag(metaTag['dataQuality'])

    if dq_elem is None:
        tree.addRootChildxmlTag(metaTag['dataQuality'])
        # add data quality element
        tree.findaddmissingxmltagNoPrint(metaTag['dataLineage'])
    else:
        # add data quality element
        tree.findaddmissingxmltagNoPrint(metaTag['dataLineage'])

    # add new process step element
    tree.addxmlTag(metaTag['dataLineage'], 'prcStep')
    prcStepElems = tree.findxmltagAll(metaTag['prcStep'])
    newprcStepElem = prcStepElems[-1]

    # add prcess step desc elemement
    addChildElemandText(newprcStepElem, metaTag['stepDesc'].split("/")[-1], stepDesc)

    # add prcess step date elemement
    if validate(prcDate):
        tempdate = prcDate + "T00:00:00"
        addChildElemandText(newprcStepElem, metaTag['stepDateTm'].split("/")[-1], tempdate)
    else:
        tempdate = ""

    # set new step prcessor elemement
    stepProcElem = meta.ET.Element(metaTag['stepProc'].split("/")[-1])

    # add processor contact
    for j in elemList:
        if TEMPLATE[j] != "":
            findaddmissingxmltag(stepProcElem, responsibleparty[j])
            tempStepProcElem = stepProcElem.find(responsibleparty[j])
            tempStepProcElem.text = TEMPLATE[j]

    roleElem = meta.ET.Element('role')
    meta.ET.SubElement(roleElem, 'RoleCd').set('value', TEMPLATE["contRole"])
    stepProcElem.append(roleElem)

    # add step processor element to process step
    newprcStepElem.append(stepProcElem)

    # update revised date
    dateupdate(metaTag["revisedate"], tempdate)

    # write changes back to xml file
    tree.writeXml(xml_file)

    if (inputdesc.dataType == 'File') & (input_meta.lower().endswith('.xml')):
        exit()
    else:
        arcpy.AddMessage("  # Process: Import Metadata")
        arcpy.MetadataImporter_conversion(xml_file, input_meta)

        # synchronize metadata
        arcpy.AddMessage("  # Process: Synchronize Metadata")
        arcpy.SynchronizeMetadata_conversion(input_meta, "SELECTIVE")

arcpy.AddMessage(" ")