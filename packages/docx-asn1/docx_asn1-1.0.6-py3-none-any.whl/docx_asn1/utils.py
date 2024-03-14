from docx import Document
from sys import argv, stderr
from os.path import isfile


def extract_text_from_docx(filename):
    """extract asn1 from a docx file"""
    if not isfile(filename):
        print(f"File {filename} not found", file=stderr)
        return None
    doc = Document(filename)
    full_text = []
    inside_range = False
    for para in doc.paragraphs:
        if "-- ASN1START" in para.text:
            inside_range = True
            continue
        elif "-- ASN1STOP" in para.text:
            inside_range = False
            continue

        # Add the paragraph text if inside the desired range
        if inside_range:
            full_text.append(para.text)
    return "\n".join(full_text)


def main():
    """main function"""
    if len(argv) < 2:
        print("Usage: python decode_asn1.py <filename>", file=stderr)
        print("Or: python decode_asn1.py <filename> <outputfile>", file=stderr)
        return
    extracted_text = extract_text_from_docx(argv[1])
    if extracted_text is None:
        return
    if len(argv) > 2:
        output_filename = argv[2]
        with open(output_filename, "w", encoding="utf-8") as file:
            file.write(extracted_text)
    else:
        print(extracted_text)
