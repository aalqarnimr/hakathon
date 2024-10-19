import pymupdf
import arabic_reshaper

def extract_text_from_pdf(pdf_file):
    with pymupdf.open(pdf_file) as doc:
        text = ""
        for page in doc:
            page_text = page.get_text("text")
            #reshaped_text = arabic_reshaper.reshape(page_text)
            text += page_text
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

pdf_path = "ijar.pdf"
output_file = "extracted_text.txt"
arabic_text = extract_text_from_pdf(pdf_path)

save_text_to_file(arabic_text, output_file)
