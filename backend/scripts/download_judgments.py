"""
Download sample Karnataka HC judgment PDFs for demo.
Uses publicly available judgment PDFs.
Run: python scripts/download_judgments.py
"""
import os
import requests

SAMPLE_PDFS = [
    {
        "url": "https://www.kslaw.in/uploads/verdicts/WP_No_200771_2015.pdf",
        "filename": "KHC_WP_Sample_1.pdf"
    },
    {
        "url": "https://api.judis.nic.in/pdfdoc/KHC/2024/KHC2024_0001.pdf",
        "filename": "KHC_WP_Sample_2.pdf"
    }
]

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "sample-judgments")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_demo_pdf(filename: str, case_number: str, department: str, directive: str, days: int):
    """Create a demo PDF with realistic judgment text using reportlab if available, else plain text."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
        from datetime import datetime, timedelta

        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        order_date = (datetime.now() - timedelta(days=30)).strftime("%d.%m.%Y")
        due_date = (datetime.now() + timedelta(days=days)).strftime("%d.%m.%Y")

        content = [
            f"IN THE HIGH COURT OF KARNATAKA AT BENGALURU",
            f"(Before Hon'ble Justice S.R. Krishna Kumar)",
            f"WRIT PETITION NO. {case_number} OF 2024",
            f"BETWEEN:",
            f"Rajesh Kumar S/o Venkatesh ... Petitioner",
            f"AND",
            f"State of Karnataka & Ors. ... Respondents",
            f"",
            f"Date of Order: {order_date}",
            f"",
            f"ORDER",
            f"",
            f"This writ petition is filed under Articles 226 and 227 of the Constitution of India praying to direct the respondents to consider the representation of the petitioner.",
            f"",
            f"Having heard the learned counsel for the parties and perused the records, this Court is of the considered opinion that the petitioner's grievance deserves to be redressed.",
            f"",
            f"ACCORDINGLY, the writ petition is disposed of with the following directions:",
            f"",
            f"1. The {directive}",
            f"",
            f"2. The respondent {department} shall file a compliance report before this Court within {days} days.",
            f"",
            f"3. Failure to comply with the above directions shall be viewed seriously by this Court.",
            f"",
            f"The Registry is directed to list this matter for compliance on {due_date}.",
            f"",
            f"Sd/-",
            f"JUDGE",
        ]

        for line in content:
            story.append(Paragraph(line if line else "&nbsp;", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

        doc.build(story)
        print(f"✅ Created PDF: {filename}")
    except ImportError:
        # Fallback: create a text file if reportlab not available
        with open(filepath.replace('.pdf', '.txt'), 'w') as f:
            f.write(f"SAMPLE JUDGMENT - {case_number}\n\n")
            f.write(f"ORDER\n\n")
            f.write(f"1. {directive}\n\n")
            f.write(f"2. The {department} shall file compliance within {days} days.\n")
        print(f"⚠️  Created text file (install reportlab for PDF): {filename.replace('.pdf','.txt')}")

if __name__ == "__main__":
    print("Creating sample Karnataka HC judgment PDFs...")

    samples = [
        ("WP_45821_2024_Revenue.pdf", "45821", "Revenue Department",
         "Secretary, Revenue Department is directed to regularise the services of the petitioner within 30 days from the date of this order.", 30),
        ("WP_12334_2024_Urban.pdf", "12334", "Urban Development Department",
         "Commissioner, BBMP is hereby directed to remove the illegal encroachments on survey number 142 forthwith.", 7),
        ("WP_67890_2023_Education.pdf", "67890", "Education Department",
         "Director of Public Instruction shall ensure that all government school teachers are paid their pending salaries within 45 days.", 45),
        ("WP_33201_2024_Health.pdf", "33201", "Health Department",
         "Commissioner of Health and Family Welfare Services is directed to fill up the vacant posts of doctors in government hospitals within 60 days.", 60),
        ("WP_19847_2024_PWD.pdf", "19847", "Public Works Department",
         "Chief Engineer, PWD must complete the construction of the approach road to the village within 90 days.", 90),
    ]

    for filename, case_num, dept, directive, days in samples:
        create_demo_pdf(filename, case_num, dept, directive, days)

    print(f"\nSample files saved to: {OUTPUT_DIR}")
    print("Install reportlab for actual PDFs: pip install reportlab")
