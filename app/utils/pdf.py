from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
def md_to_simple_pdf(md_text: str, out_path: str):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4
    x, y = 20*mm, height - 20*mm
    for line in md_text.splitlines():
        if y < 20*mm:
            c.showPage()
            y = height - 20*mm
        c.drawString(x, y, line)
        y -= 7*mm
    c.save()
