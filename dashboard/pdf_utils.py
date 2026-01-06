from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_admin_pdf(context):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        "<b>Admin Analytics Summary</b>",
        styles['Title']
    ))

    elements.append(Paragraph(
        f"Total Assessments: {context['total_assessments']}",
        styles['Normal']
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
