# makePDF

This is a simple script to convert a markdown file to convert all images or pdfs in a directory to a single pdf file.

## Usage

```bash
makePDF [operation] [flags]
```

## Operations

- `img`: Convert all images in a directory to a single PDF.
- `pdf`: Convert all PDFs in a directory to a single PDF.
- `help`: Display help information.

## Flags

- `-name`: The name of the output file.
- `-in` or `--input`: The input directory.
- `-out` or `--output`: The output directory.

## Example

Merge images from the directory `input_images` into a single PDF named `output.pdf` in the directory `example/output_pdf`:

```bash
makePDF img -in input_images -out example/output_pdf -name output.pdf
```

Merge all pdf in the current directory into a single PDF in the current directory:

```bash
makePDF.py pdf
```

## Installation

```bash
pip install img-to-pdf
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Motivation

I created this script in an afternoon because I was not having a fun time converting images to PDFs for class. [Automator](https://apple.stackexchange.com/questions/12709/how-can-i-convert-jpg-into-pdf-easily) has a good solution for Mac users, but I was more comfortable in the terminal.

## Room for Improvement

- Add support for other file types.
- Further Optimization

