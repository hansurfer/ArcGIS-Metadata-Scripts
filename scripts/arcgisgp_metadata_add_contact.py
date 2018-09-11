import os
import arcpy
import xml.etree.ElementTree as ET

addresstype = {'Postal': 'postal', 'Physical':'physical', 'Both':'both', 'Empty':''}
role = {
    'Resource Provider': '001',
    'Custodian':'002',
    'Owner':'003',
    'User':'004',
    'Distributor':'005',
    'Originator':'006',
    'Point of Contact':'007',
    'Principal Investigator':'008',
    'Processor':'009',
    'Publisher':'010',
    'Author':'010',
    'Empty':''
}

inputmetadata = arcpy.GetParameterAsText(0)
contacttype = arcpy.GetParameterAsText(1)
indName = arcpy.GetParameterAsText(2)
orgName = arcpy.GetParameterAsText(3)
posName = arcpy.GetParameterAsText(4)
contPhone = arcpy.GetParameterAsText(5)
contFax = arcpy.GetParameterAsText(6)
contAdddrs = arcpy.GetParameterAsText(7)
contAddrs = arcpy.GetParameterAsText(8)
contCity = arcpy.GetParameterAsText(9)
contAdmAa = arcpy.GetParameterAsText(10)
contZip = arcpy.GetParameterAsText(11)
contEmail = arcpy.GetParameterAsText(12)
contHours = arcpy.GetParameterAsText(13)
contInstr = arcpy.GetParameterAsText(14)
contRole = arcpy.GetParameterAsText(15)

inputmetadata_list = [metas.replace("'", "") for metas in inputmetadata.split(";")]


# disable geoprocessing history logging
arcpy.SetLogHistory(False)


def xmlout(inputPar):
    # set arcpy Describe object from input
    inputdesc = arcpy.Describe(inputPar)
    # check input file is xml
    if (inputdesc.dataType == 'File') & (inputPar.lower().endswith('.xml')):
        return inputPar
    # check input data element is in the list
    elif inputdesc.dataType in ["FeatureClass", "Table", "Workspace", "ShapeFile", "FeatureDataset"]:
        return xmlExport(inputPar)
    else:
        arcpy.AddMessage("Please select an input from xml, shapefile, feature class, feature dataset, Table, or Workspace")
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
    output_xml = os.path.join(out_dir, os.path.basename(fc) + ".xml")
    #XSLT transforamtion
    arcpy.XSLTransform_conversion(fc, xslt, output_xml)
    return output_xml


def addxmlTag(parentxmltag, chilxmlele):
    """Append child xml element"""
    child_element = ET.Element(chilxmlele)
    parent_element = tree.find(parentxmltag)
    parent_element.append(child_element)


def findaddmissingxmltag(inputTag):
    """
    Check input (xml) tag exist in xml file.
    If not, add missing element (xml tag)
    NO Print statement
    """
    # xml elements list
    xml_element_list = inputTag.split("/")
    # xml root
    xmlRoot = tree.getroot()

    for j in range(len(xml_element_list), 0, -1):
        # recreate xml tag from xml elements list
        xmltag = "/".join(xml_element_list[0:j])

        # find and add missing child element/tag
        if tree.find(xmltag) is not None:
            temp_xml_tag = xmltag
            for k in range(j, len(xml_element_list)):
                childxml = xml_element_list[k]
                addxmlTag(temp_xml_tag, childxml)
                temp_xml_tag = "/".join(xml_element_list[0:k+1])
            break
        # add if input element/tag doesn't exist
        if j-1 == 0:
            child_element = ET.Element(xmltag)
            xmlRoot.append(child_element)
            temp_xml_tag = xmltag
            for l in range (1, len(xml_element_list)):
                childxml = xml_element_list[l]
                addxmlTag(temp_xml_tag, childxml)
                temp_xml_tag = "/".join(xml_element_list[0:l+1])


def constrContact(conElement):
    if indName:
        indNameElem = ET.SubElement(conElement, "rpIndName")
        indNameElem.text = indName
    if orgName:
        orgNameElem = ET.SubElement(conElement, "rpOrgName")
        orgNameElem.text = orgName
    if posName:
        posNameElem = ET.SubElement(conElement, "rpPosName")
        posNameElem.text = posName

    if contPhone or contFax or contAdddrs or contAddrs or contCity or contAdmAa or contZip or contEmail or contHours or contInstr:
        cntInfoElem = ET.SubElement(conElement, "rpCntInfo")

    if contPhone or contFax:
        cntPhoneElem = ET.SubElement(cntInfoElem, "cntPhone")
    if contPhone:
        voiceNumElem = ET.SubElement(cntPhoneElem, "voiceNum")
        voiceNumElem.text = contPhone
    if contFax:
        faxNumElem = ET.SubElement(cntPhoneElem, "faxNum")
        faxNumElem.text = contFax

    if (addresstype[contAdddrs] != '') or contAddrs or contCity or contAdmAa or contZip or contEmail:
        # contAdddrsElem = ET.SubElement(cntInfoElem, "cntAddress", {'addressType': addresstype[contAdddrs]})
        contAdddrsElem = ET.SubElement(cntInfoElem, "cntAddress")
    if (addresstype[contAdddrs] != ''):
        contAdddrsElem.set('addressType', addresstype[contAdddrs])
    if contAddrs:
        delPointElem = ET.SubElement(contAdddrsElem, 'delPoint')
        delPointElem.text = contAddrs
    if contCity:
        cityElem = ET.SubElement(contAdddrsElem, 'city')
        cityElem.text = contCity
    if contAdmAa:
        adminAreaElem = ET.SubElement(contAdddrsElem, 'adminArea')
        adminAreaElem.text = contAdmAa
    if contZip:
        postCodeElem = ET.SubElement(contAdddrsElem, 'postCode')
        postCodeElem.text = contZip
        # countryElem = ET.SubElement(contAdddrsElem, 'country')
        # countryElem.text = contCnty
    if contEmail:
        eMailAddElem = ET.SubElement(contAdddrsElem, 'eMailAdd')
        eMailAddElem.text = contEmail

    if contHours:
        cntHoursElem = ET.SubElement(contAdddrsElem, 'cntHours')
        cntHoursElem.text = contHours
    if contInstr:
        contInstrElem = ET.SubElement(contAdddrsElem, 'cntInstr')
        contInstrElem.text = contInstr

    if role[contRole] != '':
        roleElem = ET.SubElement(conElement, 'role')
        rolecdElem = ET.SubElement(roleElem, 'RoleCd', {'value': role[contRole]})


for index, inputmeta in enumerate(inputmetadata_list):
    inputmeta = inputmeta.replace("'", "")
    # set input basename
    baseName = os.path.basename(inputmeta)
    arcpy.AddMessage("\n{} of {}: {}".format(index + 1, len(inputmetadata_list), baseName))
    # set input xml file
    inputxml = xmlout(inputmeta)

    tree = ET.parse(inputxml)
    root = tree.getroot()

    if contacttype == "Resource Point of Contact":
        # set resource contact elem
        resContElem = tree.find('dataIdInfo')
        # create new contact info element
        contactTopElem = ET.Element('idPoC')
        constrContact(contactTopElem)
        # insert new contract info
        resContElem.insert(len(resContElem), contactTopElem)

    elif contacttype == "Citation Contact":
        # set citation contact elem
        citContElem = tree.find('dataIdInfo/idCitation')
        if citContElem is None:
            findaddmissingxmltag('dataIdInfo/idCitation')
        # create new contact info element
        contactTopElem = ET.Element('citRespParty')
        constrContact(contactTopElem)
        citContElem.insert(len(citContElem), contactTopElem)

    elif contacttype == "Metadata Contact":
        # set metadata contact elem
        mdContElem = ET.Element('mdContact')
        constrContact(mdContElem)
        root.insert(len(root), mdContElem)

    elif contacttype == "Distributor Contact":
        # set distributor contact elem
        disContElem = tree.find('distInfo/distributor')
        if disContElem is None:
            findaddmissingxmltag('distInfo/distributor')
        # create new contact info element
        contactTopElem = ET.Element('distorCont')
        constrContact(contactTopElem)
        disContElem.insert(len(disContElem), contactTopElem)

    tree.write(inputxml)

    # set input data arcpy Describe object
    tardesc = arcpy.Describe(inputmeta)
    # check if input data type is in the list
    if tardesc.datatype in ["FeatureClass", "Table", "Workspace", "ShapeFile", "FeatureDataset"]:
        # import metadata back to feature class
        arcpy.MetadataImporter_conversion(inputxml, inputmeta)
        # synchronize metadata
        arcpy.SynchronizeMetadata_conversion(inputmeta, "SELECTIVE")

arcpy.AddMessage(" ")