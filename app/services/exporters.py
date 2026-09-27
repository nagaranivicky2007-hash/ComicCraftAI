import os
import requests
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def save_pdf(panels, output_path):
    os.makedirs("generated", exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story_flow = []

    # Title for submission
    story_flow.append(Paragraph("<b><font size=20>ComicCraft AI - Generated Comic</font></b>", styles['Title']))
    story_flow.append(Spacer(1, 15))
    story_flow.append(Paragraph(f"<font size=10>Story: {panels[0]['text'][:150]}...</font>", styles['Normal']))
    story_flow.append(Spacer(1, 20))

    for i, p in enumerate(panels, 1):
        try:
            print(f"PDF: Downloading panel {i}/4")
            # Headers to avoid blocking
            r = requests.get(p['image_url'], timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
            r.raise_for_status()
            img_path = f"generated/temp_panel_{i}.jpg"
            with open(img_path, 'wb') as f:
                f.write(r.content)

            story_flow.append(Paragraph(f"<b>Panel {i}: {p.get('title','')}</b>", styles['Heading2']))
            story_flow.append(Spacer(1, 5))
            story_flow.append(RLImage(img_path, width=450, height=300, kind='proportional'))
            story_flow.append(Spacer(1, 5))
            story_flow.append(Paragraph(p.get('text',''), styles['Normal']))
            story_flow.append(Spacer(1, 25))
        except Exception as e:
            print(f"Panel {i} PDF error: {e}")
            # Even if image fails, text will be in PDF - PDF open aagum
            story_flow.append(Paragraph(f"<b>Panel {i}: {p.get('title','')}</b> - {p.get('text','')}", styles['Normal']))
            story_flow.append(Spacer(1, 20))

    doc.build(story_flow)
    print(f"PDF SUCCESS: {output_path} - READY FOR SUBMISSION")
    return output_path