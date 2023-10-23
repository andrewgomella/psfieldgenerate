"""
Generate powerscribe autotext fields from RDE or RDE sets 
- uses json files from https://www.radelement.org/
- uses psReportGenerator.py for psReport class
- rough proof of concept
- tested with python 3.10.7 64-bit, Windows 11, powerscribe v4.0 SP1 (build 7.0.111.20)

Some notes:
- newline and tab characters are removed entirely from json to prevent formatting issues (noting in rare instances they may be desired)
- default value handling:
    - numeric - 0
    - string - ""
    - picklist - chooses first value

11/2022 andrew.gomella@jefferson.edu
"""
import argparse
from xml.dom import minidom
import glob
import json
from psReportGenerator import psReport


def rdeJsonToRTF(rdeJson, report, prefix):
    """
    Add single json rde to report instance
    """

    if prefix == True:
        report.addText(rdeJson['name']+': ')

    _field = {'name': rdeJson['name'],
              'type': '',
              'choices': []}
    if "float_values" in rdeJson or "integer_values" in rdeJson:
        _field['type'] = 'Numeric'
        # todo- more sophisticated default numeric
        _field['defaultvalue'] = "0"
        report.addField(_field)
    elif "value_set" in rdeJson:
        _field['type'] = 'PickList'
        for idx, value in enumerate(rdeJson['value_set']['values']):
            _choice = {'name': value['name'], 'value': value['name']}
            if idx == 0:
                # set default value
                _field['defaultvalue'] = value['name']
            # _choice={'name':value['name'] , 'value':value['value']}
            _field['choices'].append(_choice)
        report.addField(_field)
    elif "string_values" in rdeJson:
        _field['type'] = 'Text'
        _field['defaultvalue'] = ''
        report.addField(_field)
    elif "boolean_values" in rdeJson:
        # treat boolean field as picklist
        _field['type'] = 'PickList'
        _field['defaultvalue'] = 'False'
        _field['choices'] = [{'name': 'False', 'value': 'False'}, {
            'name': 'True', 'value': 'True'}]
        report.addField(_field)
    else:
        # likely incomplete RDE
        print('Error, unrecognized RDE style.')
        return None
    return report


def singleJsonToRTF(jsonFilePath, prefix=True):
    """
    Generic function to handle RDE json
    - accept json file path
    """
    try:
        with open(jsonFilePath, encoding='utf8') as jsonfile:
            jsonInput = json.load(jsonfile)
        print("\n\"" + jsonFilePath + "\"" + ' loaded')
    except FileNotFoundError:
        print("Wrong file or file path")
        return

    # hack to fix problem characters/formatting issues
    jsonString = json.dumps(jsonInput, ensure_ascii=False)
    # jsonString = jsonString.replace('\u00b2', '^2')
    # jsonString = jsonString.replace('\u00b3', '^3')
    jsonString = jsonString.replace(r'\t', '')
    jsonString = jsonString.replace(r'\n', '')
    jsonInput = json.loads(jsonString)

    if "data" in jsonInput:
        jsonInput = jsonInput["data"]

    _report = psReport(reportName=jsonInput["id"])
    print('\t initialized class with id ' + jsonInput["id"])
    if 'elements' in jsonInput:
        # we are dealing with a 'set' of elements
        if True:
            _report.addText(
                jsonInput['name'] + ' (' + jsonInput["id"] + ')', paragraphAtEnd=True)
        for element in jsonInput['elements']:
            # print(element)
            _report = rdeJsonToRTF(element, _report, prefix)
            if _report == None:
                break
    else:
        # we likely just have a single element
        _report = rdeJsonToRTF(jsonInput, _report, prefix)
    if _report != None:
        return _report
    else:
        print(' error generating report likely unexpected rde json')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        epilog='Input json file name containing one RSNA RDE or one RSNA RDES (set),  output will be printed to file named (CDE#).rtf in output folder' +
        '\n To include a prefix followed by a semicolon before the field add the argument --prefix' +
        '\n To attempt to generate autotext from all json in directory use --folder')
    parser.add_argument('--jsonfile', type=str, required=False)
    parser.add_argument('--inputfolder', type=str, required=False)
    parser.add_argument('--outputfolder', type=str, required=False)
    parser.add_argument('--prefix', action='store_true', required=False)

    args = parser.parse_args()
    prefix = True if args.prefix else False
    outputfolder = "." if args.outputfolder is None else args.outputfolder

    if args.inputfolder:
        # turn all json in dir to rtf
        jslist = glob.glob(args.inputfolder+"//*.json")
        for file in jslist:
            print(file)
            report = singleJsonToRTF(jsonFilePath=file, prefix=prefix)
            if report != None:
                report.outputFile(folder=outputfolder)
    elif args.jsonfile:
        report = singleJsonToRTF(jsonFilePath=args.jsonfile, prefix=prefix)
        if report != None:
            report.outputFile(folder=outputfolder)
    else:
        print('Error invalid input')
    print(outputfolder)
