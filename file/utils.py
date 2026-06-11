from fpdf import FPDF
import tempfile
import os

def detect_drug_category(drug_name):
    """Automatically detects drug category based on predefined lists."""
    if not drug_name:
        return "Others"
        
    drug_name_lower = drug_name.lower().strip()
    
    categories = {
        "NSAID / Analgesic": ["paracetamol", "ibuprofen", "diclofenac", "aspirin"],
        "Antibiotic": ["amoxicillin", "azithromycin", "ciprofloxacin", "metronidazole"],
        "Antiallergic / Antihistamine": ["cetirizine", "loratadine", "diphenhydramine", "chlorpheniramine"],
        "Antidiabetic": ["metformin", "glipizide", "insulin"],
        "Antihypertensive": ["amlodipine", "atenolol", "losartan", "ramipril"]
    }
    
    for category, drugs in categories.items():
        if any(d in drug_name_lower for d in drugs):
            return category
            
    return "Others"

def generate_report_pdf(report_data):
    """Generates a PDF file for a given report and returns the file path."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Title
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(200, 10, txt="Adverse Drug Reaction (ADR) Report", ln=True, align='C')
    pdf.ln(10)
    
    # Content
    pdf.set_font("Helvetica", size=12)
    
    fields_to_print = [
        ("Report ID", report_data.get('report_id', 'N/A')),
        ("Submission Date", str(report_data.get('submission_timestamp', 'N/A'))),
        ("Final Category", report_data.get('final_drug_category', 'N/A')),
        ("Patient Name", report_data.get('patient_name', 'N/A')),
        ("Patient Email", report_data.get('patient_email', 'N/A')),
        ("Patient Mobile", report_data.get('patient_mobile', 'N/A')),
        ("Age", str(report_data.get('age', 'N/A'))),
        ("Gender", report_data.get('gender', 'N/A')),
        ("Weight (kg)", str(report_data.get('weight_kg', 'N/A'))),
        ("Drug Name", report_data.get('drug_name', 'N/A')),
        ("Indication", report_data.get('indication', 'N/A')),
        ("Medicine Start Date", report_data.get('medicine_start_date', 'N/A')),
        ("Medicine Stop Date", report_data.get('medicine_stop_date', 'N/A')),
        ("Reaction Start Date", report_data.get('reaction_start_date', 'N/A')),
        ("Reaction End Date", report_data.get('reaction_end_date', 'N/A')),
        ("Reaction Description", report_data.get('reaction_description', 'N/A')),
        ("Route of Administration", report_data.get('route_of_administration', 'N/A')),
        ("Strength", report_data.get('strength', 'N/A')),
        ("Frequency", report_data.get('frequency', 'N/A')),
        ("Batch Number", report_data.get('batch_number', 'N/A')),
        ("Expiry Date", report_data.get('expiry_date', 'N/A')),
        ("Action Taken", report_data.get('action_taken', 'N/A')),
        ("Physician Name", report_data.get('physician_name', 'N/A')),
        ("Physician Contact", report_data.get('physician_contact', 'N/A')),
    ]
    
    for label, value in fields_to_print:
        # Handle empty/None values
        val_str = str(value) if value is not None and value != "" else "N/A"
        # Write to PDF
        # encode to latin-1 and ignore errors to avoid fpdf issues with unicode
        safe_label = label.encode('latin-1', 'replace').decode('latin-1')
        safe_val = val_str.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.set_font("Helvetica", style="B", size=12)
        pdf.cell(50, 10, txt=f"{safe_label}:", ln=False)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, txt=safe_val)
        
    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"ADR_Report_{report_data.get('report_id', 'new')}.pdf")
    pdf.output(file_path)
    
    return file_path
