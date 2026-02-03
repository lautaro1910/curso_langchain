from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        # Logo or Title
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CV Analysis Report / Reporte de Análisis de CV', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    """
    Sanitize text to be compatible with Latin-1 encoding (standard FPDF fonts).
    Removes unsupported characters like emojis.
    """
    if not isinstance(text, str):
        return str(text)
    
    # Encode to latin-1, ignoring characters that cannot be encoded (like emojis)
    # Then decode back to string
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf_report(analysis_result, lang_code, translations):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title and Date
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True, align='R')
    pdf.ln(10)

    # Candidate Profile
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["profile_header"]), ln=True, align='L')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=clean_text(f"{translations[lang_code]['lbl_name']} {analysis_result.name_candidate}"), ln=True)
    pdf.cell(200, 10, txt=clean_text(f"{translations[lang_code]['lbl_exp']} {analysis_result.years_of_experience}"), ln=True)
    
    edu_text = ", ".join(analysis_result.education) if isinstance(analysis_result.education, list) else str(analysis_result.education)
    pdf.multi_cell(0, 10, txt=clean_text(f"{translations[lang_code]['lbl_edu']} {edu_text}"))
    pdf.ln(5)

    # Evaluation
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["results_header"]), ln=True, align='L')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=clean_text(f"{translations[lang_code]['eval_match']}: {analysis_result.percentage_match}%"), ln=True)
    pdf.ln(5)

    # Experience
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["exp_header"]), ln=True, align='L')
    pdf.set_font("Arial", size=11)
    
    if isinstance(analysis_result.experience, list):
        for exp in analysis_result.experience:
            pdf.multi_cell(0, 10, txt=clean_text(f"- {exp}"))
    else:
        pdf.multi_cell(0, 10, txt=clean_text(str(analysis_result.experience)))
    pdf.ln(5)

    # Skills
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["skills_header"]), ln=True, align='L')
    pdf.set_font("Arial", size=11)
    if analysis_result.abilities:
        for skill in analysis_result.abilities:
            pdf.cell(0, 8, txt=clean_text(f"- {skill}"), ln=True)
    else:
        pdf.cell(0, 8, txt=clean_text(translations[lang_code]["no_skills"]), ln=True)
    pdf.ln(5)

    # Strengths
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["strengths_header"]), ln=True, align='L')
    pdf.set_font("Arial", size=11)
    if analysis_result.strengths:
        for strength in analysis_result.strengths:
            pdf.cell(0, 8, txt=clean_text(f"- {strength}"), ln=True)
    else:
        pdf.cell(0, 8, txt=clean_text(translations[lang_code]["no_strengths"]), ln=True)
    pdf.ln(5)

    # Areas for Improvement
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt=clean_text(translations[lang_code]["areas_header"]), ln=True, align='L')
    pdf.set_font("Arial", size=11)
    if analysis_result.areas_for_improvement:
        for area in analysis_result.areas_for_improvement:
            pdf.cell(0, 8, txt=clean_text(f"- {area}"), ln=True)
    else:
        pdf.cell(0, 8, txt=clean_text(translations[lang_code]["no_areas"]), ln=True)
    pdf.ln(5)

    # Return binary data
    # Note: 'S' returns the document as a string. We encode it to bytes.
    # We must ensure the return value is bytes for streamlit download_button
    return pdf.output(dest='S').encode('latin-1')
