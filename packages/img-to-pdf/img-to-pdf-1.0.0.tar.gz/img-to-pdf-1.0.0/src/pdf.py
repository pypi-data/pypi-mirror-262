import os
import img2pdf
from PyPDF2 import PdfMerger
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

register_heif_opener()

def create_valid_filepath(outdir, filepath):
    if not os.path.exists(os.path.join(outdir, filepath)):
        return filepath
    
    print(f"Error: File {filepath} already exists in {outdir}")
    i = 1
    while os.path.exists(os.path.join(outdir, f"{filepath[:-4]}_{i}.pdf")):
        i += 1
    filepath = f"{filepath[:-4]}_{i}.pdf"
    print(f"Using {filepath} instead")
    return filepath

def write_pdf_to_file(pdf, filepath):
    with open(filepath, 'wb') as output_file:
        pdf.write(output_file)


def merge_pdfs_in_directory(indir='./', outdir='./', output_filename='merged.pdf'):
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)

    output_filename = create_valid_filepath(outdir, output_filename)
    
    os.chdir(indir)
    
    merger = PdfMerger()

    for filename in os.listdir('.'):
        if filename.endswith('.pdf'):
            filepath = os.path.join(indir, filename)
            if os.path.getsize(filepath) > 0:
                merger.append(filepath)

    if len(merger.pages) == 0:
        print(f"No non-empty PDFs found in {indir}. Aborting operation.")
        return
    if len(merger.pages) == 1:
        print(f"Only one non-empty PDF found in {indir}. No need to merge.")
        return

    output_filepath = os.path.join(outdir, output_filename)
    with open(output_filepath, 'wb') as output_file:
        merger.write(output_file)

    print(f"All non-empty PDFs in {indir} have been merged into {output_filepath}.")
    print(f"PDFs combined: {len(merger.pages)}")

def merge_images_to_pdf(indir='./', outdir='./', output_filename='merged_images.pdf'):
    indir = os.path.abspath(indir)
    outdir = os.path.abspath(outdir)

    output_filename = create_valid_filepath(outdir, output_filename)
    
    os.chdir(indir)

    images = [os.path.join(indir, filename) for filename in os.listdir('.') if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.heic', '.tiff'))]

    valid_images = []
    invalid_images = []

    for image in tqdm(images, desc="Processing images"):
        try:
            with Image.open(image) as img:
                img.verify()
            valid_images.append(image)
        except (IOError, SyntaxError):
            invalid_images.append(image)

    if invalid_images:
        print(f"Warning: The following images could not be read and will be skipped:")
        for img in invalid_images:
            print(img)

    if not valid_images:
        print(f"No valid images found in {indir}. Aborting operation.")
        return

    print(f"Converting {len(valid_images)} images to PDF...")
    pdf_bytes = img2pdf.convert(valid_images)

    output_filepath = os.path.join(outdir, output_filename)
    with open(output_filepath, 'wb') as output_file:
        output_file.write(pdf_bytes)
    
    print(f"All images in {indir} have been merged into {output_filepath}.")
    print(f"Images combined: {len(valid_images)}")

