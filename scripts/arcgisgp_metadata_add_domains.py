# Purpose: add attribute domains to metadata

import os
import collections

import sl_meta_functs as meta
from sl_meta_functs import arcpy
from ArcGIS_metadata_tags import metaTag, dataDictionary, codedDomain, rangeDomain

dataDictionary = collections.OrderedDict(dataDictionary)
codedDomain = collections.OrderedDict(codedDomain)
rangeDomain = collections.OrderedDict(rangeDomain)

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
    xslt = dir + "Metadata\\Stylesheets\\gpTools\\exact copy of.xslt"
    # set output directory
    out_dir = arcpy.env.scratchFolder
    # set arcpy workspace
    arcpy.env.workspace = out_dir
    # set workspace overwrite true
    arcpy.env.overwriteOutput = True
    #assemble output xml file name
    output_xml = os.path.join(out_dir, os.path.basename(fc) + ".xml")
    if os.path.isfile(output_xml):
        output_xml = output_xml.replace(".xml", "_1.xml")
    #XSLT transforamtion
    arcpy.XSLTransform_conversion(fc, xslt, output_xml)
    return output_xml


def domainDict(ws):
    arcpy.env.workspace = ws
    # dictionary - {domain name lowercase: {code value: code desc}}
    coded_dict, range_dict = {}, {}
    domains = arcpy.da.ListDomains(ws)
    for domain in domains:
        # meta.printit('Domain name : {0}'.format(domain.name))
        if domain.domainType == 'CodedValue':
            coded_values = domain.codedValues
            temp_dict = {}
            for val, desc in coded_values.items():
                # meta.printit('{0} : {1}'.format(val, desc))
                temp_dict[val] = desc
            coded_dict[domain.name.lower()] = temp_dict
        elif domain.domainType == 'Range':
            temp_dict = {}
            temp_dict['min'] = domain.range[0]
            temp_dict['max'] = domain.range[1]
            range_dict[domain.name.lower()] = temp_dict

    return coded_dict, range_dict


def addedomainElem(domainattrElem, domaindefsour):
    """
    add coded domains

    Parameters
    ----------
    domainattrElem: Element (XML)
        Domain attribute element
    domaindefsour: String
        Domain source definition
    Returns
    -------
    """
    domainname = fieldswithedomain[fieldname]
    # coded domain
    domaincodelist = edomaindicts[domainname]
    # set new attrdomv element
    attrdomvElem = meta.ET.Element(dataDictionary["descvalue"])

    # loop coded domain
    for ecodeddomain in domaincodelist.keys():
        # new edom element
        edomElem = meta.ET.Element(dataDictionary["edomain"])

        # new edomv element
        domainvElem = meta.ET.Element(codedDomain["value"])
        domainvElem.text = str(ecodeddomain)
        # append elements
        edomElem.append(domainvElem)

        # new edomvd element
        domaindElem = meta.ET.Element(codedDomain["desc"])
        domaindElem.text = domaincodelist[ecodeddomain]
        # append elements
        edomElem.append(domaindElem)

        # new edomvds element
        if domaindefsource:
            domaindsElem = meta.ET.Element(codedDomain["descs"])
            domaindsElem.text = domaindefsour
            # append elements
            edomElem.append(domaindsElem)

        attrdomvElem.append(edomElem)

    domainattrElem.append(attrdomvElem)


def addrdomainElem(domainattrElem):
    """
    add range domains

    Parameters
    ----------
    domainattrElem: Element (XML)
        Domain attribute element
    Returns
    -------
    """
    domainname = fieldswithrdomain[fieldname]
    # range domain
    domainranage = rdomaindicts[domainname]
    # set new attrdomv element
    attrdomvElem = meta.ET.Element(dataDictionary["descvalue"])

    # new edom element
    rdomElem = meta.ET.Element(dataDictionary["rdomain"])
    # new rdommin element
    domainminElem = meta.ET.Element(rangeDomain["min"])
    domainminElem.text = str(domainranage["min"])
    # new rdommax element
    domainmaxElem = meta.ET.Element(rangeDomain["max"])
    domainmaxElem.text = str(domainranage["max"])

    # append elements
    rdomElem.append(domainminElem)
    rdomElem.append(domainmaxElem)
    attrdomvElem.append(rdomElem)
    domainattrElem.append(attrdomvElem)


sourcemetadata = arcpy.GetParameterAsText(0)
source_metadatas = sourcemetadata.split(";")
ws = arcpy.GetParameterAsText(1)
domaindefsource = arcpy.GetParameterAsText(2)

meta.setscratchWS()

edomaindicts, rdomaindicts = domainDict(ws)

for dataset in source_metadatas:
    dataset = dataset.replace("'", "")
    if arcpy.Exists(dataset):
        sourceXML = xmlout(dataset)
        sourcetree = meta.xmlMeta(sourceXML)
        desc = arcpy.Describe(dataset)
        fields = arcpy.ListFields(dataset)
        # dictionary - {field name lowercase: domain name lowercase}
        fieldswithedomain, fieldswithrdomain = {}, {}
        for field in fields:
            if field.domain.lower() in edomaindicts:
                fieldswithedomain[field.name.lower()] = field.domain.lower()
            elif field.domain.lower() in rdomaindicts:
                fieldswithrdomain[field.name.lower()] = field.domain.lower()

        # all attribute elements
        source_attrElem = sourcetree.findxmltagAll(metaTag["eainfoattr"])
        source_attrElem_dict = {elem.find(dataDictionary['fieldname']).text.lower():elem for elem in source_attrElem}

        for attrElem in source_attrElem:
            # find field name attrbiute elements
            attrlabelElem = attrElem.find(dataDictionary["fieldname"])
            # field name
            fieldname = attrlabelElem.text.lower()

            # if field name is in domain field name list
            if fieldname in fieldswithedomain:
                addedomainElem(attrElem, domaindefsource)
            elif fieldname in fieldswithrdomain:
                addrdomainElem(attrElem)

        sourcetree.writeXml(sourceXML)
        # import metadata back to feature class
        meta.arcpy.MetadataImporter_conversion(sourceXML, dataset)

meta.deletescratchgdb()