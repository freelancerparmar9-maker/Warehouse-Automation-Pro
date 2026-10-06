import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def create_pdf(filepath, title_text, po_number, items, is_invoice):
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title and PO Number
    elements.append(Paragraph(title_text, styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>PO Number:</b> {po_number}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Determine headers based on document type
    if is_invoice:
        headers = ['Item Code', 'Description', 'Quantity', 'Unit Price']
    else:
        headers = ['Item Code', 'Description', 'Quantity']

    table_data = [headers] + items
    
    # Table styling
    t = Table(table_data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    elements.append(t)
    doc.build(elements)

if __name__ == '__main__':
    output_dir = 'sample_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Pair 1: Everything matches
    po1 = 'PO-45672'
    inv_data_1 = [
        ['ITM-001', 'Steel Bolts M8', '100', '$10.00'], 
        ['ITM-002', 'Nylon Washers', '200', '$5.00']
    ]
    pl_data_1 = [
        ['ITM-001', 'Steel Bolts M8', '100'], 
        ['ITM-002', 'Nylon Washers', '200']
    ]
    create_pdf(os.path.join(output_dir, f'Invoice_{po1}.pdf'), 'INVOICE', po1, inv_data_1, True)
    create_pdf(os.path.join(output_dir, f'PackingList_{po1}.pdf'), 'PACKING LIST', po1, pl_data_1, False)

    # Pair 2: Quantity mismatch (packing list is lower than invoice)
    po2 = 'PO-45673'
    inv_data_2 = [
        ['ITM-003', 'Packing Tape', '50', '$2.00'], 
        ['ITM-004', 'Bubble Wrap', '20', '$15.00']
    ]
    pl_data_2 = [
        ['ITM-003', 'Packing Tape', '50'], 
        ['ITM-004', 'Bubble Wrap', '15']  # Lower quantity
    ]
    create_pdf(os.path.join(output_dir, f'Invoice_{po2}.pdf'), 'INVOICE', po2, inv_data_2, True)
    create_pdf(os.path.join(output_dir, f'PackingList_{po2}.pdf'), 'PACKING LIST', po2, pl_data_2, False)

    # Pair 3: Item missing entirely from the packing list
    po3 = 'PO-45674'
    inv_data_3 = [
        ['ITM-005', 'Cardboard Boxes', '500', '$1.50'], 
        ['ITM-006', 'Shipping Labels', '1000', '$0.05'], 
        ['ITM-007', 'Marker Pens', '50', '$3.00']
    ]
    pl_data_3 = [
        ['ITM-005', 'Cardboard Boxes', '500'], 
        # Missing ITM-006
        ['ITM-007', 'Marker Pens', '50']
    ]
    create_pdf(os.path.join(output_dir, f'Invoice_{po3}.pdf'), 'INVOICE', po3, inv_data_3, True)
    create_pdf(os.path.join(output_dir, f'PackingList_{po3}.pdf'), 'PACKING LIST', po3, pl_data_3, False)

    # Sample 4: Invoice only (no packing list)
    po4 = 'PO-45675'
    inv_data_4 = [
        ['ITM-008', 'Pallet Jack', '1', '$350.00'], 
        ['ITM-009', 'Safety Goggles', '25', '$12.00']
    ]
    create_pdf(os.path.join(output_dir, f'Invoice_{po4}.pdf'), 'INVOICE', po4, inv_data_4, True)

    print("Successfully generated 4 sets of sample PDFs in the 'sample_data' folder.")
