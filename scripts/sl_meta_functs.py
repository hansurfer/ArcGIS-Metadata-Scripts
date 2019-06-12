#-------------------------------------------------------------------------------
# Purpose: metadata and xml helper module
#-------------------------------------------------------------------------------

# import modules
import arcpy
import xml.etree.ElementTree as ET
from os import path
import tempfile


def setscratchWS():
    tempdir = tempfile.gettempdir()
    scragdb = path.join(tempdir, 'scratch.gdb')
    if arcpy.Exists(scragdb):
        arcpy.Delete_management(scragdb)
    arcpy.CreateFileGDB_management(tempdir, 'scratch')
    arcpy.env.scratchWorkspace = tempdir


def deletescratchgdb():
    tempdir = tempfile.gettempdir()
    scragdb = path.join(tempdir, 'scratch.gdb')
    if arcpy.Exists(scragdb):
        arcpy.Delete_management(scragdb)


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
    output_xml = path.join(out_dir, path.basename(fc) + ".xml")
    #XSLT transforamtion
    arcpy.XSLTransform_conversion(fc, xslt, output_xml)
    return output_xml

def parentTagFuc(childTag):
    """
    Return parent tag

    Parameters
    ----------
    childTag: str
        child tag string
    Returns
    -------
    str
        return parent tag
    """
    """Get parent tag"""
    templist = childTag.split("/")
    del templist[-1:]
    return "/".join(templist)

def printit(inMessage):
    print (inMessage)
    arcpy.AddMessage(inMessage)


class xmlMeta(object):
    ##    # arcgis metadata xml tags
    ##    arcgis = tags.arcgisTag()

    def __init__(self, xmlfile):
        """

        :rtype: object
        """
        self.tree = ET.parse(xmlfile)

    def getroot(self):
        """
        Return XML root element

        Returns
        -------
        element
            XML root element
        """
        return self.tree.getroot()

    def remove(self, subelement):
        """
        Remove sub-elemennt from the input element

        Parameters
        ----------
        subelement: xml element

        Returns
        -------
        None
        """
        self.tree.remove(subelement)

    def insert(self, index, subelement):
        """
        Inserts a subelement at the given position in this element.

        Parameters
        ----------
        index: int
            a position in this element
        subelement: element
            a subelement be inserted
        Returns
        -------
        None
        """
        self.tree.insert(index, subelement)

    def findxmltag(self, inputxmltag):
        """
        Finds the first subelement matching inputxmltag. inputxmltag is a tag name. Returns an element instance or None.

        Parameters
        ----------
        inputxmltag: str
            xml tag

        Returns
        -------
        element
        """
        return self.tree.find(inputxmltag)

    def findxmltagAll(self, inputxmltag):
        """
        Finds all matching subelement by tag name. Returns a list containing all matching elements in document order.

        Parameters
        ----------
        inputxmltag: str
            xml tag

        Returns
        -------
        list
            a list containing all matching elements in document order
        """
        return self.tree.findall(inputxmltag)

    def findxmltext(self, inputxmltag):
        """Find xml element text"""
        xmltag = self.findxmltag(inputxmltag)
        return xmltag.text

    def setXmlText(self, inputxmltag, xmltext):
        """Set xml text"""
        elem = self.findxmltag(inputxmltag)
        elem.text = xmltext

    def addxmlTag(self, parentxmltag, chilxmltag):
        """Append child xml element"""
        child_element = ET.Element(chilxmltag)
        parent_element = self.findxmltag(parentxmltag)
        parent_element.append(child_element)

    def addRootChildxmlTag(self, chilxmlele):
        """Append child xml element of Root"""
        child_element = ET.Element(chilxmlele)
        parent_element = self.getroot()
        parent_element.append(child_element)

    def addxmlTagText(self, parentxmltag, chilxmltag, text=""):
        """Append child xml element and text"""
        child_element = ET.Element(chilxmltag)
        child_element.text = text
        parent_element = self.findxmltag(parentxmltag)
        parent_element.append(child_element)

    def addxmlText(self, xmltag, text=""):
        """Add xml text"""
        element = self.findxmltag(xmltag)
        element.text = text

    def addTagAtt(self, tag, key, value):
        """set the attribute key on the element to value
        tag: xml tag
        key: attribute key
        value: attribute value
        """
        elem = self.findxmltag(tag)
        elem.set(key, value)

    def deletexmlTag(self, parentTag, childTag):
        """
        Delete xml tag
        ref: http://stackoverflow.com/questions/2666436/xml-remove-child-node-of-a-node"""
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            #find child tags - a list with child Elements
            childElem = elem.findall(childTag)
            k = 0
            #loop Element and remove child elements
            for child in childElem:
                elem.remove(child)
                k += 1
            printit("total {} deleted".format(k))
        #else
        else:
            printit("Parent tag doesn't exist")

    def deletexmlTagNoPrint(self, parentTag, childTag):
        """
        Delete xml tag. No print statement
        """
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            #find child tags - a list with child Elements
            childElem = elem.findall(childTag)
            #loop Element and remove child elements
            for child in childElem:
                elem.remove(child)

    def deletexmlTag2(self, childTag):
        """
        Delete xml tag without parent tag
        """
        #get parent tag
        parentTag = parentTagFuc(childTag)
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            #find child tags - a list with child Elements
            ##            childElem = self.findxmltagAll(childTag)
            childElem = self.tree.findall(childTag)
            k = 0
            #loop Element and remove child elements
            for child in childElem:
                elem.remove(child)
                k += 1
            printit ("total {} deleted".format(k))
        #else
        else:
            printit("Parent tag doesn't exist")

    def deletexmlTag2NoPrint(self, childTag):
        """
        Delete xml tag without parent tag
        No print statement
        """
        #get parent tag
        parentTag = parentTagFuc(childTag)
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            #find child tags - a list with child Elements
            ##            childElem = self.findxmltagAll(childTag)
            childElem = self.tree.findall(childTag)
            #loop Element and remove child elements
            for child in childElem:
                elem.remove(child)

    def deleterootxmlTag(self, rootTag):
        """
        Delete root level xml tag
        """
        root = self.tree.getroot()
        elems = self.tree.findall(rootTag)
        k = 0
        #loop and remove child elements
        for elem in elems:
            root.remove(elem)
            k += 1
        printit ("total {} deleted".format(k))

    def deleterootxmlTagNoPrint(self, rootTag):
        """
        Delete root level xml tag
        No print statement
        """
        root = self.tree.getroot()
        elems = self.tree.findall(rootTag)
        #loop and remove child elements
        for elem in elems:
            root.remove(elem)

    def deleteAllChildXmlTag(self, parentTag):
        """
        Delete all child xml tag(s)
        """
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            k = 0
            #loop Element and remove child elements
            for childElem in elem:
                elem.remove(childElem)
                k += 1
            printit ("total {} deleted".format(k))
        #else
        else:
            printit("Parent tag doesn't exist")

    def deleteAllChildXmlTagNoPrint(self, parentTag):
        """
        Delete all child xml tag(s).
        NO print statement
        """
        #find parent tag - Element object
        elem = self.tree.find(parentTag)
        #if parent tag element exists
        if elem is not None:
            #loop Element and remove child elements
            for childElem in elem:
                elem.remove(childElem)

    def findreplacexmltext(self, inputxmltag, replacetext):
        """Find xml element text and replace it with given text """
        xmltext = self.findxmltext(inputxmltag)
        if xmltext is None:
            xmltext = str(xmltext)
        xmltext2 = xmltext.replace(xmltext, replacetext)
        self.tree.find(inputxmltag).text = xmltext2

    def findaddmissingxmltag(self, inputTag):
        """
        Check input (xml) tag exist in xml file.
        If not, add missing element (xml tag)
        """
        # check if input xml element/tag exist
        if self.findxmltag(inputTag) is not None:
            printit("# Tag exists: {}".format(inputTag))
            return

        printit("# Tag doesn't exist, adding: {}".format(inputTag))
        # xml elements list
        xml_element_list = inputTag.split("/")
        # xml root
        xmlRoot = self.tree.getroot()

        for j in range(len(xml_element_list), 0, -1):
            # recreate xml tag from xml elements list
            xmltag = "/".join(xml_element_list[0:j])

            # find and add missing child element/tag
            if self.findxmltag(xmltag) is not None:
                printit ("# Found matching parent xml tag: {}".format(xmltag))
                temp_xml_tag = xmltag
                for k in range(j, len(xml_element_list)):
                    childxml = xml_element_list[k]
                    printit ("Adding element: {}".format(childxml))
                    self.addxmlTag(temp_xml_tag, childxml)
                    temp_xml_tag = "/".join(xml_element_list[0:k+1])
                break
            # add if input element/tag doesn't exist
            if j-1 == 0:
                child_element = ET.Element(xmltag)
                xmlRoot.append(child_element)
                temp_xml_tag = xmltag
                for l in range (1, len(xml_element_list)):
                    childxml = xml_element_list[l]
                    printit ("Adding element: {}".format(childxml))
                    self.addxmlTag(temp_xml_tag, childxml)
                    temp_xml_tag = "/".join(xml_element_list[0:l+1])

    def findaddmissingxmltagNoPrint(self, inputTag):
        """
        Check input (xml) tag exist in xml file.
        If not, add missing element (xml tag)
        NO Print statement
        """
        # check if input xml element/tag exist
        if self.findxmltag(inputTag) is not None:
            return

        # xml elements list
        xml_element_list = inputTag.split("/")
        # xml root
        xmlRoot = self.tree.getroot()

        for j in range(len(xml_element_list), 0, -1):
            # recreate xml tag from xml elements list
            xmltag = "/".join(xml_element_list[0:j])

            # find and add missing child element/tag
            if self.findxmltag(xmltag) is not None:
                temp_xml_tag = xmltag
                for k in range(j, len(xml_element_list)):
                    childxml = xml_element_list[k]
                    self.addxmlTag(temp_xml_tag, childxml)
                    temp_xml_tag = "/".join(xml_element_list[0:k+1])
                break
            # add if input element/tag doesn't exist
            if j-1 == 0:
                child_element = ET.Element(xmltag)
                xmlRoot.append(child_element)
                temp_xml_tag = xmltag
                for l in range (1, len(xml_element_list)):
                    childxml = xml_element_list[l]
                    self.addxmlTag(temp_xml_tag, childxml)
                    temp_xml_tag = "/".join(xml_element_list[0:l+1])

    def writeXml(self, xmlfile):
        self.tree.write(xmlfile)