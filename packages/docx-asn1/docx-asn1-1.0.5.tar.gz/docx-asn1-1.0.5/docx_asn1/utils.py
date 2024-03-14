from docx import Document
from sys import argv


def extract_text_from_docx(filename):
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
    # Get the first .docx file name in the current directory
    # check argv[1] to get the path
    if len(argv) < 2:
        print("Usage: python decode_asn1.py <filename>")
        print("Or: python decode_asn1.py <filename> <outputfile>")
        exit(1)
    extracted_text = extract_text_from_docx(argv[1])
    if len(argv) > 3:
        filename = argv[2]
        with open(filename, "w", encoding="utf-8") as file:
            file.write(extracted_text)
    else:
        print(extracted_text)
