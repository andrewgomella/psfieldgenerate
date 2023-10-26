# psfieldgenerate

This project consists of three python scripts, and will be presented as part of an Education Exhibit at [RSNA 2023](https://www.rsna.org/annual-meeting). 

- `psReportGenerator.py` - a python class for dynamic generation of Powerscribe reports/macros
- `rdeToPsReport.py` - python command line script to convert RadElement.org json into Powerscribe reports/macros via psReportGenerator class above
- `downloadSets.py` - a script to batch download elements from [radelement.org](https://www.radelement.org/) 

# rdeToPsReport.py

This command-line program is designed to generate PowerScribe AutoText fields from RSNA RDE (Radiological Society of North America Report Data Elements) or RDES (Report Data Element Sets). It utilizes JSON files from [radelement.org](https://www.radelement.org/) and relies on the `psReport` class provided by the included `psReportGenerator.py` script. The program is a rough proof of concept and was tested with Python 3.10.7 on a 64-bit Windows 11 environment and PowerScribe version 4.0 SP1 (build 7.0.111.20) as of November 2022.

## Usage

### Prerequisites

Before using this program, ensure you have the required JSON files containing RSNA RDE or RDES data. You can obtain these files from [radelement.org](https://www.radelement.org/). Alternatively you can use the included script `download_sets.py` to batch download them.

### Command-Line Arguments

The program accepts the following command-line arguments:

- `--jsonfile`: The path to a JSON file containing a single RSNA RDE or RDES. If provided, the program will generate an AutoText based on this file. Alternatively specify an input folder to specify a folder of json files.
- `--inputfolder`: The path to a folder containing multiple JSON files. If provided, the program will attempt to generate AutoTexts for all the JSON files in the folder.
- `--outputfolder`: The folder where the generated RTF files will be saved. If not provided, the RTF files will be saved in the current directory.
- `--prefix`: An optional flag. If specified, a prefix followed by a semicolon will be added before each field in the generated AutoText. This is likely always desired. 

### Output

The program will generate Rich Text Format (RTF) compatible with Powerscribe. Each RTF file will be named based on the RDE's ID and saved in the specified output folder.

## Example

To generate an AutoText from a single JSON file and specify a prefix for the fields, you can use the following command:

```bash
python power_scribe_autotext_generator.py --jsonfile input.json --outputfolder output --prefix
```

This will generate an RTF file in the "output" folder, incorporating the specified prefix.

To process all JSON files in a folder, use the `--inputfolder` argument:

```bash
python power_scribe_autotext_generator.py --inputfolder input_folder --outputfolder output --prefix
```

This command will create RTF files for each JSON file in the "input_folder" and save them in the "output" folder.

## Notes

- The program removes all newline and tab characters from the JSON to prevent formatting issues. However, be aware that in some rare instances, these characters may be desired.

- Default field selections for different field types are as follows:
  - Numeric: 0
  - String: ""
  - PickList: Chooses the first value in the list


# `psReportGenerator.py` psReport Class 

This Python class, `psReport`, is a utility for generating PowerScribe reports with AutoText fields. It is a rough proof of concept that supports "Text," "Numeric," and "PickList" field types. It has been tested with Python 3.10.7 on a 64-bit Windows 11 environment and PowerScribe version 4.0 SP1 (build 7.0.111.20) as of November 2022.

## Overview

The `psReport` class represents when instantiated represents an entire PowerScribe report (and/or AutoText). It allows you to add plain text and various types of fields to the report. The class takes care of generating the necessary Rich Text Format (RTF) and XML elements to create the final RTF file, which can then be dragged and dropped into Powerscribe or loaded separately. The primary features of this class are as follows:

- Adding plain text blocks to the report.
- Generating the necessary RTF and XML for various field types ("Text," "Numeric," and "PickList").
- Outputting an RTF file as either bytes or text

## Usage

1. **Initialization**: Create an instance of the `psReport` class, optionally specifying the report name.

    ```python
    auto_text = psReport("MyReport")
    ```

2. **Adding Plain Text**: You can add plain text to the report using the `addText` method. Optionally, you can specify whether to create a new paragraph at the end of the added text.

    ```python
    auto_text.addText("This is plain text.", paragraphAtEnd=True)
    ```

3. **Adding Fields**: You can add fields to the report using the `addField` method. The method supports "Text," "Numeric," and "PickList" field types.

    ```python
    field_data = {
        'name': 'MyField',
        'type': 'Text',  # or 'Numeric' or 'PickList'
        'choices': ['Choice1', 'Choice2'],
        'defaultvalue': 'Choice1'
    }
    auto_text.addField(field_data)
    ```

4. **Generating the AutoText**: To generate the RTF and XML representation of the AutoText, you can use the `outputBytes` method to get the RTF as bytes, or the `outputText` method to get the RTF as a string with XML included.

    ```python
    rtf_bytes = auto_text.outputBytes()
    rtf_text = auto_text.outputText()
    ```
5. **XML Preview**: To see the XML representation of the AutoText, you can use the `printXML` method.

    ```python
    auto_text.printXML()
    ```
    
7. **Saving to a File**: You can save the AutoText to an RTF file using the `outputFile` method.

    ```python
    auto_text.outputFile(filename='output_folder/my_report.rtf')
    ```

## Example

Here's a simple example of how to use the `psReport` class to generate an AutoText with plain text and a PickList field:

```python
# Create an AutoText instance
auto_text = psReport("MyReport")

# Add plain text
auto_text.addText("This is plain text.", paragraphAtEnd=True)

# Define field data
field_data = {
    'name': 'MyField',
    'type': 'PickList',
    'choices': ['Choice1', 'Choice2'],
    'defaultvalue': 'Choice1'
}

# Add a PickList field
auto_text.addField(field_data)

# Generate and save the AutoText
auto_text.outputFile(filename='output_folder/my_report.rtf')
```

This will create an AutoText with plain text and a PickList field and save it as an RTF file.

Please note that this is a basic implementation and may require further customization to meet specific AutoText requirements in PowerScribe. The class generates RTF and XML structures that are used in PowerScribe, and additional customization may be needed for more complex AutoText templates.

## Credit
Thanks to Adam Flanders, MD, both for the original idea/concept and help testing this project. 
