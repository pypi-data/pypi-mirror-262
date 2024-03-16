bizextract
==========
Simple script for extracting business data from PDFs.

Requirements
------------
* [Python](https://www.python.org/)
* [Java](https://aws.amazon.com/corretto/)

Installation (with pip)
-----------------------
1. `pip install bizextract`

Usage
-----
From a terminal or command prompt:
```shell
> bizextract -h
usage: bizextract - a tool to extract business data from PDF reports. [-h] [--pattern PATTERN] output

positional arguments:
  output             The output path (or file) to write the results. Content will be a CSV file.

options:
  -h, --help         show this help message and exit
  --pattern PATTERN  A file name pattern to limit the files parsed by the tool.
```

Please note the pattern option can be used to select files for parsing. The default is to search the current folder for
the common file name pattern given when downloading the reports. When all else fails just add only the reports to a folder
and change directories in the terminal to that folder, then run the tool like below in the example.

Example
------
```shell
> bizextract --pattern *.pdf output.csv
```