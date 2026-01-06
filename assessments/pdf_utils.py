from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

def generate_assessment_pdf(user, assessments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(
        "<b>Digital Mental Health Support System</b><br/>Assessment Report",
        styles['Title']
    ))

    elements.append(Paragraph(
        f"Student Username: {user.username}",
        styles['Normal']
    ))

    elements.append(Paragraph(" ", styles['Normal']))

    table_data = [
        ["Test", "Score", "Severity", "Date"]
    ]

    for a in assessments:
        table_data.append([
            a.test_type,
            str(a.score),
            a.severity,
            a.created_at.strftime("%d %b %Y %H:%M")
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ]))

    elements.append(table)

    elements.append(Paragraph(
        "<br/><i>This report is for self-assessment and educational purposes only.</i>",
        styles['Italic']
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
