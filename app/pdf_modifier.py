from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

def add_text_to_template(template_path, texts, output_path):
    template_pdf = PdfReader(template_path)
    output_pdf = PdfWriter()

    overlay = BytesIO()
    c = canvas.Canvas(overlay)

    for text in texts:
        x, y, content = text["x"], text["y"], text["content"]
        c.drawString(x, y, content)

    c.save()
    overlay.seek(0)

    overlay_pdf = PdfReader(overlay)

    for page_num in range(len(template_pdf.pages)):
        template_page = template_pdf.pages[page_num]
        overlay_page = overlay_pdf.pages[0]

        template_page.merge_page(overlay_page)
        output_pdf.add_page(template_page)

    with open(output_path, "wb") as output_file:
        output_pdf.write(output_file)
