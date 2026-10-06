---
tools:
  - name: filesystem
---

# Skill: Local Warehouse Auditor

## Description
A local-only high-precision auditor that reconciles Packing Lists against Invoices and logs discrepancies to a local CSV file.

## Operational Guardrails
1. **Local Isolation**: All data processing must stay on this machine.
2. **Verbose Logging**: You MUST print a message to the console for every file you scan.

## Reconciliation Logic
1. **Scan**: List all PDFs in `D:/Warehouse_Audit_Pending`. **Print "Scanning folder D:/Warehouse_Audit_Pending..." and then print the names of files found.**
2. **Reconcile**: Compare Invoice vs. Packing List. **Print "Comparing [File A] and [File B]...".**
3. **Local Logging**: Append results directly to `D:/Audit_Report.csv`.
4. **Archiving**: Move processed files to `D:/Warehouse_Audit_Completed`.

