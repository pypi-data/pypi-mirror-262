import os, sys
from src.pdf import merge_images_to_pdf, merge_pdfs_in_directory

operation_map = {"img": merge_images_to_pdf, "pdf": merge_pdfs_in_directory}
help_map = {"img": "merge images in the input directory into a single PDF file", 
            "pdf": "merge PDFs in the input directory into a single PDF file", 
            "help": "prints this message or prints further information about a certain flag or command", 
            "-i": "specifies the absolute path to the input directory (where the images or PDFs are located)", 
            "--input": "specifies the absolute path to the input directory (where the images or PDFs are located)",
            "-o": "specifies the absolute path to the output directory (where the pdf will be generated)", 
            "--output": "specifies the absolute path to the output directory (where the pdf will be generated)",
            "-name": "the name of the output file",
            }

def is_valid_flag(flag):
    return flag.startswith("-") and help_map.get(flag) is not None

def validate_flag_arg(flag, arg):
    if not is_valid_flag(flag):
        print(f"Flag {flag} not found. Please use 'help' to see the available flags.")
        sys.exit(1)
    if arg.startswith("-"):
        print(f"Did you forget to specify the argument for {flag}? Got: '{arg}'.\nPlease use 'help' to see the available flags.")
        sys.exit(1)
    if flag != "-name" and not os.path.isdir(arg):
        print(f"Directory {arg} not found.")
        response = input("Would you like to create it? (y/n): ")
        if response.lower() == "y":
            os.makedirs(arg)
        else:
            print("You did not create the directory. Aborting operation.")
            sys.exit(1)

def map_flags(args):
    flags = {}
    for i in range(1, len(args)):
        if is_valid_flag(args[i]):
            validate_flag_arg(args[i], args[i+1])
            flags[args[i]] = args[i+1]
    return flags

def generate_help_message():
    help_message = """
makePDF: A simple tool to manipulate files
------------------------------------------

Operations:
-----------

img -in <input_directory> -out <output_directory> -name <output_filename>
    Merge images in the input directory into a single PDF file.

pdf -in <input_directory> -out <output_directory> -name <output_filename>
    Merge PDFs in the input directory into a single PDF file.

help <command or flag>
    Print this message or further information about a specific command or flag.
    Example: help -in

Arguments:
----------

-i, --input <input_directory>
    Specify the input directory containing files to be processed. Default is the current directory.

-o, --output <output_directory>
    Specify the output directory where the merged PDF file will be saved. Default is the current directory.

-name, <output_filename>
    Specify the name of the output PDF file. Default is 'merged.pdf' for PDF merging and 'merged_images.pdf' for image merging.

Example usage:
--------------

Merge images:
    makePDF img -in /path/to/input_directory -out /path/to/output_directory -name my_merged_images.pdf

Merge PDFs:
    makePDF pdf -in /path/to/input_directory -out /path/to/output_directory -name my_merged.pdf

Get help:
    makePDF help
    makePDF help -in
"""

    return help_message