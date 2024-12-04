# Merging multiple PDF files

import PyPDF2
import pdfplumber
import fitz  # PyMuPDF

def merge_pdfs(pdf_list, output_path):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_path, 'wb') as out:
        pdf_writer.write(out)
    print(f"Merged PDF saved as {output_path}")
def split_pdf(pdf_path, output_dir, pages_per_file):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)
    
    for i in range(0, total_pages, pages_per_file):
        pdf_writer = PyPDF2.PdfWriter()
        
        for j in range(i, min(i + pages_per_file, total_pages)):
            pdf_writer.add_page(pdf_reader.pages[j])
        
        output_path = f"{output_dir}/split_{i // pages_per_file + 1}.pdf"
        with open(output_path, 'wb') as out:
            pdf_writer.write(out)
        print(f"Saved {output_path}")
def extract_text(pdf_path, output_text_path):
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + '\n'
        # Sử dụng mã hóa UTF-8 để lưu tệp
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"Extracted text is saved as {output_text_path}")

def extract_images(pdf_path, output_dir):
    pdf_document = fitz.open(pdf_path)

    for page_index in range(len(pdf_document)):
        page = pdf_document.load_page(page_index)
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"{output_dir}/image_{page_index+1}_{img_index+1}.{image_ext}"
            
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
                print(f"Đã lưu hình ảnh: {image_filename}")


# merge_pdfs(['Chữa ETS 2022 - Listening.pdf', 'Chữa ETS 2022 - Reading.pdf'], 'D:\\Python_Project\\Web-Scraping_Web-Crawling\\PDFTool\\Merged_Document.pdf')
# split_pdf("D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\Merged_Document.pdf", "D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\SplitFolder", 30)
# extract_text("D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\SplitFolder\split_1.pdf","D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\GetTextFromPDF\Output.txt")
extract_images("D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\SplitFolder\split_1.pdf","D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\GetImagePdf")
