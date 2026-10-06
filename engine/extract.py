import os
import glob
import pdfplumber

def extract_pdf(path):
    """
    Extracts po_number, doc_type, and items from a given PDF.
    Returns a dictionary with the extracted data or an error message.
    """
    result = {
        'file': os.path.basename(path),
        'doc_type': 'unknown',
        'po_number': 'unknown',
        'items': []
    }
    
    try:
        with pdfplumber.open(path) as pdf:
            if not pdf.pages:
                return {'file': result['file'], 'error': 'PDF file is empty or has no pages.'}
            
            # Assuming the main data is on the first page for these documents
            page = pdf.pages[0]
            
            # 1. Extract Text for doc_type and po_number
            text = page.extract_text()
            if not text:
                return {'file': result['file'], 'error': 'Could not extract any text from the PDF.'}
                
            text_upper = text.upper()
            if 'INVOICE' in text_upper:
                result['doc_type'] = 'invoice'
            elif 'PACKING LIST' in text_upper:
                result['doc_type'] = 'packing_list'
                
            for line in text.split('\n'):
                if 'PO Number:' in line:
                    result['po_number'] = line.split('PO Number:')[-1].strip()
                    break
                    
            # 2. Extract Table for items
            tables = page.extract_tables()
            if not tables:
                return {'file': result['file'], 'error': 'No table found in the PDF.'}
                
            table = tables[0] # Take the first table
            if len(table) < 2:
                return {'file': result['file'], 'error': 'Table found, but it has no data rows.'}
                
            # Parse headers to dynamically find column positions
            headers = [str(h).strip().replace('\n', ' ').upper() if h else '' for h in table[0]]
            col_map = {}
            for i, h in enumerate(headers):
                if 'ITEM CODE' in h:
                    col_map['code'] = i
                elif 'DESCRIPTION' in h:
                    col_map['desc'] = i
                elif 'QUANTITY' in h:
                    col_map['qty'] = i
                elif 'UNIT PRICE' in h:
                    col_map['price'] = i
                    
            # Check if essential columns exist
            if 'code' not in col_map or 'qty' not in col_map:
                return {'file': result['file'], 'error': f'Required columns (Item Code, Quantity) missing. Found headers: {headers}'}

            # Parse item rows
            for row in table[1:]:
                # Skip entirely empty rows
                if not any(row):
                    continue
                    
                item = {
                    'item_code': str(row[col_map['code']]).strip() if row[col_map['code']] else '',
                    'description': str(row[col_map['desc']]).strip() if ('desc' in col_map and row[col_map['desc']]) else '',
                    'quantity': str(row[col_map['qty']]).strip() if row[col_map['qty']] else '',
                }
                
                if 'price' in col_map:
                    item['unit_price'] = str(row[col_map['price']]).strip() if row[col_map['price']] else ''
                else:
                    item['unit_price'] = None
                    
                result['items'].append(item)
                
        return result
        
    except Exception as e:
        return {'file': os.path.basename(path), 'error': f"Failed to extract: {str(e)}"}

if __name__ == '__main__':
    import pprint
    
    # Path resolution to handle execution from different directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, '..'))
    sample_dir = os.path.join(project_dir, 'sample_data')
    
    pdf_files = glob.glob(os.path.join(sample_dir, '*.pdf'))
    
    if not pdf_files:
        print(f"No PDFs found in {sample_dir}")
    else:
        for pdf_file in pdf_files:
            print(f"--- Extracting from {os.path.basename(pdf_file)} ---")
            extracted_data = extract_pdf(pdf_file)
            pprint.pprint(extracted_data, sort_dicts=False)
            print("\n")
