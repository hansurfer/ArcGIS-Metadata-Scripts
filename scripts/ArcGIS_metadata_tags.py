# -*- coding: utf-8 -*-

# arcgis metadata xml tags
metaTag = {
"description":      "dataIdInfo/idAbs",
"summary":          "dataIdInfo/idPurp",
"title":            "dataIdInfo/idCitation/resTitle",
"revisedate":       "dataIdInfo/idCitation/date/reviseDate",
"createdate":       "dataIdInfo/idCitation/date/createDate",
"pubDate":          "dataIdInfo/idCitation/date/pubDate",
"credit":           "dataIdInfo/idCredit",
"resConstrai":      "dataIdInfo/resConst",                      #resource contraints
"genUseLimit":      "dataIdInfo/resConst/Consts/useLimit",
"legUseLimit":      "dataIdInfo/resConst/LegConsts/useLimit",
"secUseLimit":      "dataIdInfo/resConst/SecConsts/useLimit",
"themekeys":        "dataIdInfo/themekeys",
"placekeys":        "dataIdInfo/placekeys",
"searchKeys":       "dataIdInfo/searchKeys",
"productkeys":      "dataIdInfo/productKeys",
"subTopicCatKeys":  "dataIdInfo/subTopicCatKeys",
"idSpecUse":        "dataIdInfo/idSpecUse",
"procEnviron":      "dataIdInfo/envirDesc",
"suppleminfo":      "dataIdInfo/suppInfo",
"keyword":          "keyword",
"thumbnail":        "Binary/Thumbnail/Data",
"entityName":       "eainfo/detailed/enttyp/enttypl",
"isotopic":         "dataIdInfo/tpCat/TopicCatCd",
"eainfo":           "eainfo",
"eainfoattr":       "eainfo/detailed/attr",

# Time Period of Content
"tmPosition":          "dataIdInfo/dataExt/tempEle/TempExtent/exTemp/TM_Instant/tmPosition",

# metadata format
"ArcGISformat":     "Esri/ArcGISFormat",
"ArcGISstyle":      "Esri/ArcGISstyle",
"mdStanName":       "mdStanName",

# Resource citation
"resCitation" :     "dataIdInfo/idCitation",
"dataQuality" :     'dqInfo',                                   # Data quality
"dqScope" :         'dqInfo/dqScope',                           # Data quality scope
"dqReport":         'dqInfo/report',                            # Data quality report

# Process step
"dataLineage":      'dqInfo/dataLineage',
"dataQualityDesc":  'dqInfo/report/measDesc',                   # Data quality report description
"prcStep":          'dqInfo/dataLineage/prcStep',               # process step
"stepDesc":         'dqInfo/dataLineage/prcStep/stepDesc',      # process step desc
"stepDateTm":       'dqInfo/dataLineage/prcStep/stepDateTm',    # process step date
"stepProc":         'dqInfo/dataLineage/prcStep/stepProc',      # step processor

# Distributor
"distributor":      "distInfo/distributor",
"distOrderPrc":     "distInfo/distributor/distorOrdPrc",            # Distributor's order process
"distOrderInstr":   "distInfo/distributor/distorOrdPrc/ordInstr",   # Distributor's ordering instructions
"distTranOps":      "distInfo/distTranOps",                         # Distributor's transfer options
}


#-------------- EAINFO -----------------#
dataDictionary = ([
    ("fieldname",   "attrlabl"),
    ("fielddesc",   "attrdef"),
    ("fielddescs",  "attrdefs"),
    ("descvalue",   "attrdomv"),
    ("edomain",      "edom"), # child element of attrdomv - attrdomv/edom
    ("rdomain",      "rdom"), # child element of attrdomv - attrdomv/rdom
])

codedDomain = ([
    ("value",  "edomv"),
    ("desc",   "edomvd"),
    ("descs",  "edomvds"),
])

rangeDomain = ([
    ("min",  "rdommin"),
    ("max",  "rdommax"),
])

#-------------- CONTACTS -----------------#
# In order to use the following dicts, set it as ordered dictionary
# example:
# import collections
# contacts = collections.OrderedDict(contacts)
# print (contact["resContact"])

contacts = ([
("resContact",      "dataIdInfo/idPoC"),                        # Resource point of contact
("resUserContact",  'dataIdInfo/idSpecUse/usrCntInfo'),         # Resource user contact
("resMDContact",    "dataIdInfo/resMaint/maintCont"),           # Resource Maintenance contact
("citContact",      "dataIdInfo/idCitation/citRespParty"),      # Citation Responsible party or contact
("mdContact",       "mdContact"),                               # Metadata contact
("mdMaintContact",  'mdMaint/maintCont'),                       # Metadata maintenance Contact
("distContact",     "distInfo/distributor/distorCont")          # Distributor contact
])

contactsDesc = ([
("resContact",      "Resource point of contact"),
("resUserContact",  'Resource user contact'),
("resMDContact",    "Resource Maintenance contact"),
("citContact",      "Citation Responsible party or contact"),
("mdContact",       "Metadata contact"),
("mdMaintContact",  'Metadata maintenance Contact'),
("distContact",     "Distributor contact")
])

# <responsible party elements> - Contact Info #
responsibleparty = ([
("indName",     "rpIndName"),
("orgName",     "rpOrgName"),
("posName",     "rpPosName"),
("contPhone",   "rpCntInfo/cntPhone/voiceNum"),
("contFax",     "rpCntInfo/cntPhone/faxNum"),
("contAdddrs",  "rpCntInfo/cntAddress"),
("contAddrs",   "rpCntInfo/cntAddress/delPoint"),
("contCity",    "rpCntInfo/cntAddress/city"),
("contAdmAa",   "rpCntInfo/cntAddress/adminArea"),
("contZip",     "rpCntInfo/cntAddress/postCode"),
("contCnty",    "rpCntInfo/cntAddress/country"),
("contEmail",   "rpCntInfo/cntAddress/eMailAdd"),
("contHours",   "rpCntInfo/cntHours"),
("contInstr",   "rpCntInfo/cntInstr"),
("contRole",    "role")
])

responsiblepartyDesc = ([
("indName",     "Contact individual name"),
("orgName",     "Contact organization name"),
("posName",     "Contact position name"),
("contPhone",   "Contact phone number"),
("contFax",     "Contact fax number"),
("contAdddrs",  "Contact address type"),
("contAddrs",   "Contact address delivery point"),
("contCity",    "Contact address city"),
("contAdmAa",   "Contact address administrative area, e.g. state or province"),
("contZip",     "Contact address postal/zip code"),
("contCnty",    "Contact address country"),
("contEmail",   "Contact email address"),
("contHours",   "Contact hours of operation"),
("contInstr",   "Contact instructions"),
("contRole",    "Contact's role")
])

metacheck = [
    ["description", "genUseLimit", "dataQualityDesc", "proStepDesc"],
    ["resContact", "distContact", "mdContact"],
    ["summary"]
]

constraints = ["genUseLimit", "legUseLimit", "secUseLimit"]
constraintDesc = {
    "genUseLimit": "General Constraint", 
    "legUseLimit": "Legal Constraint", 
    "secUseLimit": "Security Constraint"
}

FGDCTags = ['Esri','Binary','idinfo','dataqual','spdoinfo','spref','distinfo','metainfo','seqId','MemberName','catFetTyps','scaleDist','dimResol','valUnit','quanValUnit','coordinates','usrDefFreq','exTemp','citId','citIdType','geoBox','geoDesc','MdIdent','RS_Identifier','searchKeys']

ISOTopics = {
    '001': 'farming',
    '002': 'biota',
    '003': 'boundaries',
    '004': 'climatologyMeteorologyAtmosphere',
    '005': 'economy',
    '006': 'elevation',
    '007': 'environment',
    '008': 'geoscientificInformation',
    '009': 'health',
    '010': 'imageryBaseMapsEarthCover',
    '011': 'intelligenceMilitary',
    '012': 'inlandWaters',
    '013': 'location',
    '014': 'oceans',
    '015': 'planningCadastre',
    '016': 'society',
    '017': 'structure',
    '018': 'transportation',
    '019': 'utilitiesCommunication',
    '': 'None'
}