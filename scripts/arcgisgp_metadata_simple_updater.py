#################################################################
#       Update Metadata_Template.xml before using this tool     #
#################################################################

import os
import collections
import inspect
import base64
from time import strftime
from ArcGIS_metadata_tags import metaTag, contacts, contactsDesc, constraints
import sl_meta_functs as meta
from sl_meta_functs import arcpy

# input parameters
input_metadata = arcpy.GetParameterAsText(0)
titleinput = arcpy.GetParameterAsText(1)
searchkeywords = arcpy.GetParameterAsText(2)
summaryinput = arcpy.GetParameterAsText(3)
descinput = arcpy.GetParameterAsText(4)
creditsinput = arcpy.GetParameterAsText(5)
options = arcpy.GetParameterAsText(6)
dq = arcpy.GetParameter(7)
langcnty = arcpy.GetParameter(8)
revise = arcpy.GetParameter(9)
image = arcpy.GetParameterAsText(10)

option_list = options.split(";")

# set xml element from default xml template
# python script (current) directory
# https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory-in-python
filename = inspect.getframeinfo(inspect.currentframe()).filename
pypath = os.path.dirname(os.path.abspath(filename))
default_xml = os.path.join(pypath, "Metadata_Template.xml")
default_tree = meta.xmlMeta(default_xml)
# temp_root = temp_tree.getroot()

# local variables
contacts = collections.OrderedDict(contacts)
contactsDesc = collections.OrderedDict(contactsDesc)

# disable geoprocessing history logging
arcpy.SetLogHistory(False)


def dataidinfoupdate(elementname, tag, textinput):
    if len(textinput) > 0:
        meta.printit("# {}...".format(elementname))
        tempTag = metaTag[tag]
        # find element
        temp_elem = tree.findxmltag(tempTag)
        if temp_elem is None:
            # add tag
            tree.findaddmissingxmltagNoPrint(tempTag)
            # set new text
            tree.setXmlText(tempTag, textinput)
        else:
            # set new text
            tree.setXmlText(tempTag, textinput)


def searchkeys(searchkeywords):
    if len(searchkeywords) > 0:
        searchKeys = searchkeywords.split(",")
        meta.printit("# Search Keywords...")
        # if searchKeys tag exists, delete
        searchkeyTag = metaTag["searchKeys"]
        if tree.findxmltag(searchkeyTag) is not None:
            tree.deletexmlTagNoPrint(searchkeyTag, metaTag["keyword"])
        # add searchKeys tag
        tree.findaddmissingxmltagNoPrint(searchkeyTag)
        # add search keyword tag & text
        for i in range(len(searchKeys)):
            tree.addxmlTagText(searchkeyTag, metaTag["keyword"], searchKeys[i].strip())


def contact(contactTag):
    # code block to replace existing contacts with a default (edit Metadata_Template.xml before using this script)
    meta.printit("# {}...".format(contactsDesc[contactTag]))
    # set xml element
    target_elem = default_tree.findxmltag(contacts[contactTag])
    contact_elem = tree.findxmltag(contacts[contactTag])
    # MD contact
    if contactTag == "mdContact":
        # delete MD contact element if it exists
        if contact_elem is not None:
            tree.deleterootxmlTagNoPrint(contacts[contactTag])
        # insert default contact
        tree_root.insert(len(tree_root), target_elem)
    # Distributor contact
    elif contactTag == "distContact":
        distributor_elem = tree.findxmltag(metaTag['distributor'])
        target_distributor_elem = default_tree.findxmltag(contacts[contactTag])
        # delete distributor contact element if it exists
        if distributor_elem is not None:
            tree.deletexmlTag2NoPrint(metaTag['distributor'])
        contact_parent_tag = meta.parentTagFuc(contacts[contactTag])
        contact_parent_elem = tree.findxmltag(contact_parent_tag)
        # add distributor elems
        if contact_parent_elem is None:
            tree.findaddmissingxmltagNoPrint(contact_parent_tag)
        # insert default contact
        contact_parent_elem = tree.findxmltag(contact_parent_tag)
        contact_parent_elem.insert(0, target_distributor_elem)
    # other contacts
    else:
        if contact_elem is not None:
            tree.deletexmlTag2NoPrint(contacts[contactTag])
        contact_parent_tag = meta.parentTagFuc(contacts[contactTag])
        contact_parent_elem = tree.findxmltag(contact_parent_tag)
        # add contact elems
        if contact_parent_elem is None:
            tree.findaddmissingxmltagNoPrint(contact_parent_tag)
        # insert default contact
        contact_parent_elem = tree.findxmltag(contact_parent_tag)
        contact_parent_elem.insert(0, target_elem)


def uselimitConstraint():
    """
    Replace General Use Limitation with default.
    :return: none
    """
    meta.printit("# Constraints... ")
    genUseLimitTag = metaTag["genUseLimit"]
    default_useLimt_elem = default_tree.findxmltag(genUseLimitTag)
    constraint_elem = tree.findxmltag(genUseLimitTag)
    if constraint_elem is not None:
        tree.deletexmlTag2NoPrint(genUseLimitTag)
    # set use limitation parent tag
    constraint_parent_tag = meta.parentTagFuc(genUseLimitTag)
    # set use limitation parent element
    constraint_parent_elem = tree.findxmltag(constraint_parent_tag)
    # add use limitation parent elem if it doesn't exist
    if constraint_parent_elem is None:
        tree.findaddmissingxmltagNoPrint(constraint_parent_tag)
    # insert default use limitation
    constraint_parent_elem = tree.findxmltag(constraint_parent_tag)
    constraint_parent_elem.insert(0, default_useLimt_elem)


def orderinstruction():
    """
    Replace distribution order instruction with default.
    :return: none
    """
    meta.printit("# Order Instruction...")
    orderInstrTag = metaTag["distOrderInstr"]
    default_orderInstr_elem = default_tree.findxmltag(orderInstrTag)
    # find all order instructions
    temp_elems = tree.findxmltagAll(orderInstrTag)
    for temp_elem in temp_elems:
        if temp_elem is not None:
            # delete child nodes
            tree.deleteAllChildXmlTagNoPrint(meta.parentTagFuc(orderInstrTag))

    # set Order Instruction parent tag
    orderInstr_parent_tag = meta.parentTagFuc(orderInstrTag)
    # set Order Instruction parent element
    orderInstr_parent_elem = tree.findxmltag(orderInstr_parent_tag)
    # add Order Instruction parent elem if it doesn't exist
    if orderInstr_parent_elem is None:
        tree.findaddmissingxmltagNoPrint(orderInstr_parent_tag)
    # insert default Order Instruction
    orderInstr_parent_elem = tree.findxmltag(orderInstr_parent_tag)
    orderInstr_parent_elem.insert(0, default_orderInstr_elem)


def xmlout(inputPar):
    # set arcpy Describe object from input
    inputdesc = arcpy.Describe(inputPar)
    # check input file is xml
    if (inputdesc.dataType == 'File') & (inputPar.lower().endswith('.xml')):
        return inputPar
    # check input data element is in the list
    elif inputdesc.dataType in ["FeatureClass", "RasterDataset", "Workspace", "ShapeFile", "FeatureDataset", "Table", "TextFile"]:
        return meta.xmlExport(inputPar)
    else:
        meta.printit("Please select correct data type to export Metadata")
        quit()


def convImgBinary(imageFile):
    """
    Convert image to binary. Image format must be PNG or JPG.
    If image is PNG, it will be converted to JPG becuase ArcGIS
    thumbnail is only compatible with JPG binary
    ref: http://www.programcreek.com/2013/09/convert-image-to-string-in-python/
    ref: https://stackoverflow.com/questions/43258461/convert-png-to-jpeg-using-pillow-in-python/43258955
    """
    fileExt = meta.path.basename(imageFile).split(".")[1]
    if (fileExt == "png") | (fileExt == "gif"):
        from PIL import Image
        im = Image.open(imageFile)
        newPng = im.convert('RGB')
        newJPG = meta.path.join(arcpy.env.scratchFolder, "temp.jpg")
        newPng.save(newJPG)
        with open(newJPG, "rb") as imagefile:
            str = base64.b64encode(imagefile.read())
            return str
    elif fileExt == "jpg":
        with open(imageFile, "rb") as imagefile:
            str = base64.b64encode(imagefile.read())
            return str
    else:
        meta.printit("Please convert the image to PNG, GIF, or JPG format!")
        meta.printit("Terminating the tool.")
        exit()


def thumbnail(image):
    """
    Update thumbnail.
    :return: none
    """
    if len(image) > 0:
        # ---- THUMNAIL ----#
        meta.printit("# Replace thumbnail...")
        # check thumbnail tag exist, if not add elements
        tree.findaddmissingxmltag(metaTag["thumbnail"])
        # set thumbnail attribute
        tree.addTagAtt(metaTag["thumbnail"], "EsriPropertyType", "PictureX")
        # add thumbnail binary to metadata xml
        # convert imagery to binary and append it to xml
        tree.findreplacexmltext(metaTag["thumbnail"], convImgBinary(image))


def deleteLangCntyCode():
    """
    Delete all language and country code in keywords with thesaurus.
    :return: none
    """
    thesaLang = "thesaLang"
    parentpath = './/{}/..'.format(thesaLang)
    parentelems = tree.findxmltagAll(parentpath)
    for lang in parentelems:
        childelem = lang.find('./{}'.format(thesaLang))
        lang.remove(childelem)
    # delete remaining unpaired subTopicCatKeys and productkeys
    if tree.findxmltag(metaTag["subTopicCatKeys"]) is not None:
        tree.deletexmlTag2NoPrint(metaTag["subTopicCatKeys"])
    if tree.findxmltag(metaTag["productkeys"]) is not None:
        tree.deletexmlTag2NoPrint(metaTag["productkeys"])
    # delete idSpecUse country code
    if tree.findxmltag(metaTag["idSpecUse"]) is not None:
        tree.deletexmlTag2NoPrint(metaTag["idSpecUse"])


def reviseDate():
    """
    Update revised date as today in Citation section.
    :return: none
    """
    revisedDateTag = metaTag['revisedate']
    revisedDateElem = tree.findxmltag(revisedDateTag)
    revisedDate = strftime("%Y-%m-%d") + "T00:00:00"

    if revisedDateElem is not None:
        revisedDateElem.text = revisedDate
    else:
        tree.findaddmissingxmltagNoPrint(revisedDateTag)
        revisedDateElem = tree.findxmltag(revisedDateTag)
        revisedDateElem.text = revisedDate


def metaUpdate(xml_file):
    global tree, tree_root, i
    # set xml tree element
    tree = meta.xmlMeta(xml_file)
    tree_root = tree.getroot()
    dataidinfoupdate("Title", "title", titleinput)
    searchkeys(searchkeywords)
    dataidinfoupdate("Summary (Purpose)", "summary", summaryinput)
    dataidinfoupdate("Description (Abstract)", "description", descinput)
    dataidinfoupdate("Credits", "credit", creditsinput)
    for i in option_list:
        i = i.replace("'", "")
        if i == "Resource Contact":
            contact("resContact")
        elif i == "Distribution Contact":
            contact("distContact")
        elif i == "Metadata Contact":
            contact("mdContact")
        elif i == "Use Limitation":
            uselimitConstraint()
        elif i == "Distribution Order Instruction":
            orderinstruction()
        elif i == "All":
            uselimitConstraint()
            contact("resContact")
            contact("distContact")
            orderinstruction()
            contact("mdContact")

    # delete data quality and lineage section
    if dq:
        target_dq_elem = tree.findxmltag(metaTag['dataQuality'])
        if target_dq_elem is not None:
            meta.printit("# Delete Data Quality and Lineage...")
            tree_root.remove(target_dq_elem)

    if langcnty:
        deleteLangCntyCode()

    if revise:
        reviseDate()

    # update thumbnail
    thumbnail(image)

    # write updates to xml file
    tree.writeXml(xml_file)


# set input basename
input_metadata_name = os.path.basename(input_metadata)
meta.printit(" Updating {} Metadata".format(input_metadata_name))
# set input xml file
inputxml = xmlout(input_metadata)
# update metadata
metaUpdate(inputxml)
# set input data arcpy Describe object
tardesc = arcpy.Describe(input_metadata)
# check if input data type is in the list
if tardesc.datatype in ["FeatureClass", "RasterDataset", "Workspace", "ShapeFile", "FeatureDataset", "Table", "TextFile"]:
    # import metadata back to feature class
    arcpy.MetadataImporter_conversion(inputxml, input_metadata)
    # synchronize metadata
    arcpy.SynchronizeMetadata_conversion(input_metadata, "SELECTIVE")