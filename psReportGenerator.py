"""
Generate powerscribe autotext fields
- rough proof of concept
- supports "Text", "Numeric", "PickList"
- tested with python 3.10.7 64-bit, Windows 11, powerscribe v4.0 SP1 (build 7.0.111.20)

11/2022 andrew.gomella@jefferson.edu
"""
from xml.dom import minidom
import re
import sys

class psReport:
    """ represent entire report/autotext
        whenever adding to report:
            - count characters, increment index accordingly
        when adding a field:
            - generates RTF, counts characters
            - generates XML with appropriate start/length 
    """

    def __init__(self, reportName=""):
        self.reportName = reportName
        self.cursor = 0
        self.psFieldList = []
        self.reportText = ""
        self.initXML()
        self.initRtf()

    def addText(self, text, paragraphAtEnd=False):
        """
        add plain text to report
        """
        self.rtf += text
        if paragraphAtEnd:
            self.rtf += r'\par' + '\n'
            self.cursor += 1 #add one to account for \n
        self.cursor += len(text)

    def outputBytes(self):
        _rtf = self.rtf + '}'
        return _rtf.encode('cp1252')

    def outputText(self):
        _rtf = self.rtf + '\n' + r'}'
        _rtf += '\n' + r' {\xml}'
        _rtf += self.XMLroot.toxml() # {\xml}
        return _rtf

    def outputFile(self, filename='', folder=''):
        if filename == '':
            filename = folder + '\\' +  self.reportName + ".rtf"
        outputText = self.outputText()
        print('Generating file : ' + filename + ' with ' + str(len(self.psFieldList)) + ' field/s')
        with open(filename, 'w', encoding="utf-8") as out:
            out.write(outputText)
        # sys.stdout.write(outputText)
        # *.encode('cp1252') doesnt seem to be necessary

    def addField(self, field):
        if field['type'] == "Text":
            fieldRTF = self.generateFieldRTF(field)
            _type='1'
        elif field['type'] == "Numeric":
            fieldRTF = self.generateFieldRTF(field)
            _type='2'
        elif field['type'] == "PickList":
            fieldRTF = self.generatePickListRTF(field)
            _type='3'
        elif field['type'] == "Merge":
            _type='4'
            pass
        _rtfLength = self.getRTFlength(fieldRTF)
        self.rtf += fieldRTF 
        self.addFieldToXML(type=_type, start=self.cursor, length=_rtfLength,
                           name=field['name'], choices=field['choices'], defaultvalue=field['defaultvalue'])
        print('\t added ' + field['type'] + ' field "' + field["name"] + '" of length ' + str(_rtfLength))
        if field['type'] == "PickList":
                print('\t\t PickList choices: ' + str(len(field['choices'])) + ' default value: ' + field['defaultvalue'])
        #now that we have added, update cursor to reflect new position, with extra for new line, always added after field for now
        self.cursor += _rtfLength + 1
        self.psFieldList.append(field)

    def initRtf(self):
        rtfHeader = r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil Segoe UI;}}" + "\n"
        rtfHeader += r"{\colortbl ;\red208\green103\blue40;\red178\green34\blue34;}" + "\n"
        rtfHeader += r"{\*\generator Riched20 10.0.22621}\viewkind4\uc1 " + "\n"
        # rtfHeader += "\n" # can't be raw string for newline to work
        # rtfHeader += r"\pard\cf1\f0\fs24 "
        self.rtf = rtfHeader

    def getRTFlength(self, rtfString):
        return len(re.sub(r'(\\[^\s]+\s?)', '', rtfString))

    def generateFieldRTF(self, field): 
        # type 2? - numeric
        fieldRTFString = r"\cf2 " + field['name'] + r"\cf1\par "
        return fieldRTFString

    def generatePickListRTF(self, field):
        # this string will show in AutoTextEditor, but not in reports
        # reports will show default value
        pickListRTFString = field['name'] + r" :  \cf1 "
        pickListRTFString += r'/'.join(x['name'] for x in field['choices'])
        pickListRTFString += r'\par' + '\n' + r'\cf1 '
        return pickListRTFString

    def printXML(self):
        print(self.XMLroot.toprettyxml(indent="\t"))

    def initXML(self):
        self.XMLroot = minidom.Document()
        XMLautotext = self.XMLroot.createElement('autotext')
        XMLautotext.setAttribute('version', '2')
        XMLautotext.setAttribute('editMode', '2')
        self.XMLroot.appendChild(XMLautotext)
        self.xmlFields = self.XMLroot.createElement('fields')
        XMLautotext.appendChild(self.xmlFields)
        xmlLinks = self.XMLroot.createElement('links')
        XMLautotext.appendChild(xmlLinks)
        xmlTextSource = self.XMLroot.createElement('textSource')
        XMLautotext.appendChild(xmlTextSource)
        xmlSnippetGroups = self.XMLroot.createElement('snippetGroups')
        XMLautotext.appendChild(xmlSnippetGroups)

    def addFieldToXML(self, type, start, length, name, choices, defaultvalue):
        _field = self.XMLroot.createElement('field')
        _field.setAttribute('type', str(type))
        _field.setAttribute('start', str(start))
        _field.setAttribute('length', str(length))

        _name = self.XMLroot.createElement('name')
        _name.appendChild(self.XMLroot.createTextNode(name))
        _field.appendChild(_name)

        _defaultvalue = self.XMLroot.createElement('defaultvalue')
        _defaultvalue.appendChild(self.XMLroot.createTextNode(defaultvalue))
        _field.appendChild(_defaultvalue)

        if type == "3":
            _choices = self.XMLroot.createElement('choices')
            for choice in choices:
                _choice = self.XMLroot.createElement('choice')
                _choice.setAttribute('name', choice['name'])
                _choice.appendChild(self.XMLroot.createTextNode(choice['value']))
                _choices.appendChild(_choice)
            _field.appendChild(_choices)

            #error check that default value is one of the choices

        _customproperties = self.XMLroot.createElement('customproperties')
        properties = {'AllCaps': 'False', 'AllowEmpty': 'False', 'ImpressionField': 'False', 'DoesNotIndicateFindings': 'False', 'FindingsCodes': '', 'EnforcePickList': 'False'}
        for prop in properties:
            _prop = self.XMLroot.createElement('property')
            _propName = self.XMLroot.createElement('name')
            _propName.appendChild(self.XMLroot.createTextNode(prop))
            _prop.appendChild(_propName)
            _propValue = self.XMLroot.createElement('value')
            _propValue.appendChild(
                self.XMLroot.createTextNode(properties[prop]))
            # _propValue.
            _prop.appendChild(_propValue)
            _customproperties.appendChild(_prop)
        _field.appendChild(_customproperties)
        self.xmlFields.appendChild(_field)