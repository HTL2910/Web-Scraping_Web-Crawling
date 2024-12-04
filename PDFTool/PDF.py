# Merging multiple PDF files

import PyPDF2

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


# merge_pdfs(['Chữa ETS 2022 - Listening.pdf', 'Chữa ETS 2022 - Reading.pdf'], 'D:\\Python_Project\\Web-Scraping_Web-Crawling\\PDFTool\\Merged_Document.pdf')
split_pdf("D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\Merged_Document.pdf", "D:\Python_Project\Web-Scraping_Web-Crawling\PDFTool\SplitFolder", 30)
