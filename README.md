# psfieldgenerate

# psReport Class PowerScribe AutoText Field Generator

This Python class, `psReport`, is a utility for generating PowerScribe reports with AutoText fields. It is a rough proof of concept that supports "Text," "Numeric," and "PickList" field types. It has been tested with Python 3.10.7 on a 64-bit Windows 11 environment and PowerScribe version 4.0 SP1 (build 7.0.111.20) as of November 2022.

## Overview

The `psReport` class represents when instantiated represents an entire PowerScribe report (and/or AutoText). It allows you to add plain text and various types of fields to the report. The class takes care of generating the necessary Rich Text Format (RTF) and XML elements to create the final RTF file, which can then be dragged and dropped into Powerscribe or loaded separately. The primary features of this class are as follows:

- Adding plain text blocks to the report.
- Generating the necessary RTF and XML for various field types ("Text," "Numeric," and "PickList").
- Outputting an RTF file as either bytes or text

## Usage

To use this class, follow these steps:

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

5. **Saving to a File**: You can save the AutoText to an RTF file using the `outputFile` method.

    ```python
    auto_text.outputFile(filename='output_folder/my_report.rtf')
    ```

6. **XML Preview**: To see the XML representation of the AutoText, you can use the `printXML` method.

    ```python
    auto_text.printXML()
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
