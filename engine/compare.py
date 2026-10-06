import os
import sys
import glob

# Ensure local imports work regardless of where the script is executed from
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extract import extract_pdf

def parse_qty(val):
    """Convert quantity string to integer."""
    if not val:
        return 0
    # Remove non-numeric characters
    s = "".join(c for c in str(val) if c.isdigit() or c == '-')
    try:
        return int(s)
    except ValueError:
        return 0

def parse_price(val):
    """Convert price string to float, stripping currency symbols."""
    if not val:
        return 0.0
    s = str(val).replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        return 0.0

def compare_pdfs(sample_dir):
    """
    Scans the directory for PDFs, pairs them by PO number, and compares
    the invoice items against the packing list items.
    """
    pdf_files = glob.glob(os.path.join(sample_dir, '*.pdf'))
    pos_data = {}
    
    # 1. Group extracted data by PO Number
    for pdf_file in pdf_files:
        data = extract_pdf(pdf_file)
        if 'error' in data or data.get('po_number') == 'unknown':
            continue
            
        po = data['po_number']
        if po not in pos_data:
            pos_data[po] = {'invoice': None, 'packing_list': None}
            
        doc_type = data['doc_type']
        if doc_type in ['invoice', 'packing_list']:
            pos_data[po][doc_type] = data

    results = []
    
    # 2. Compare Invoice vs Packing List
    for po_number, docs in pos_data.items():
        inv = docs['invoice']
        pl = docs['packing_list']
        
        if not inv:
            # If we only have a packing list but no invoice
            if pl:
                for item in pl['items']:
                    recv_qty = parse_qty(item.get('quantity'))
                    results.append({
                        'po_number': po_number,
                        'item_code': item.get('item_code', ''),
                        'description': item.get('description', ''),
                        'invoiced_qty': 0,
                        'received_qty': recv_qty,
                        'unit_price': 0.0,
                        'status': 'NOT_INVOICED',
                        'amount_at_risk': 0.0
                    })
            continue
            
        inv_items_dict = {i['item_code']: i for i in inv['items'] if i.get('item_code')}
        
        # Scenario: Missing Packing List entirely
        if not pl:
            for code, item in inv_items_dict.items():
                inv_qty = parse_qty(item.get('quantity'))
                price = parse_price(item.get('unit_price'))
                amount_at_risk = (inv_qty - 0) * price if 0 < inv_qty else 0.0
                
                results.append({
                    'po_number': po_number,
                    'item_code': code,
                    'description': item.get('description', ''),
                    'invoiced_qty': inv_qty,
                    'received_qty': 0,
                    'unit_price': price,
                    'status': 'PENDING',
                    'amount_at_risk': amount_at_risk
                })
            continue
            
        # Both exist: Do item-level comparison
        pl_items_dict = {i['item_code']: i for i in pl['items'] if i.get('item_code')}
        
        # Check all items that are on the invoice
        for code, inv_item in inv_items_dict.items():
            inv_qty = parse_qty(inv_item.get('quantity'))
            price = parse_price(inv_item.get('unit_price'))
            desc = inv_item.get('description', '')
            
            if code not in pl_items_dict:
                recv_qty = 0
                status = 'MISSING'
            else:
                recv_qty = parse_qty(pl_items_dict[code].get('quantity'))
                if recv_qty == inv_qty:
                    status = 'RECEIVED'
                elif recv_qty < inv_qty:
                    status = 'SHORT_SHIPPED'
                else:
                    status = 'OVER_SHIPPED'
                    
            # amount_at_risk calculation rule
            amount_at_risk = (inv_qty - recv_qty) * price if recv_qty < inv_qty else 0.0
            
            results.append({
                'po_number': po_number,
                'item_code': code,
                'description': desc,
                'invoiced_qty': inv_qty,
                'received_qty': recv_qty,
                'unit_price': price,
                'status': status,
                'amount_at_risk': amount_at_risk
            })
            
        # Check for items that are on the packing list but not the invoice
        for code, pl_item in pl_items_dict.items():
            if code not in inv_items_dict:
                recv_qty = parse_qty(pl_item.get('quantity'))
                results.append({
                    'po_number': po_number,
                    'item_code': code,
                    'description': pl_item.get('description', ''),
                    'invoiced_qty': 0,
                    'received_qty': recv_qty,
                    'unit_price': 0.0,
                    'status': 'NOT_INVOICED',
                    'amount_at_risk': 0.0
                })
                
    return results

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, '..'))
    sample_dir = os.path.join(project_dir, 'sample_data')
    
    print("Running Comparison Engine...\n")
    results = compare_pdfs(sample_dir)
    
    if not results:
        print("No results found. Please check if sample_data contains the valid PDFs.")
    else:
        # Sort results by PO number for clean output
        results.sort(key=lambda x: (x['po_number'], x['item_code']))
        
        # Display Table
        print("-" * 125)
        header = f"{'PO NUMBER':<10} | {'ITEM CODE':<10} | {'DESCRIPTION':<20} | {'INV QTY':<7} | {'REC QTY':<7} | {'PRICE':<8} | {'STATUS':<15} | {'RISK AMT'}"
        print(header)
        print("-" * 125)
        
        pos_checked = set()
        matched_count = 0
        total_risk = 0.0
        
        for r in results:
            pos_checked.add(r['po_number'])
            if r['status'] == 'RECEIVED':
                matched_count += 1
            total_risk += r['amount_at_risk']
            
            row_str = f"{r['po_number']:<10} | {r['item_code']:<10} | {r['description'][:20]:<20} | {r['invoiced_qty']:<7} | {r['received_qty']:<7} | ${r['unit_price']:<7.2f} | {r['status']:<15} | ${r['amount_at_risk']:.2f}"
            print(row_str)
            
        print("-" * 125)
        
        # Summary
        total_rows = len(results)
        review_count = total_rows - matched_count
        
        print("\nSUMMARY:")
        print(f"  POs Checked:           {len(pos_checked)}")
        print(f"  Rows Matched:          {matched_count}")
        print(f"  Rows Needing Review:   {review_count}")
        print(f"  Total Amount at Risk:  ${total_risk:.2f}")
