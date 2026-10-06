# Warehouse Automation Pro (AuditPro Local)

A desktop application designed to automatically audit warehouse documents. It compares **Invoices** against **Packing Lists** to find discrepancies like short shipments, over shipments, or missing items, and automatically generates ready-to-send supplier dispute emails in an Excel report.

## 🚀 Features
* **Automated PDF Extraction:** Uses Python (`pdfplumber`) to accurately read Item Codes, Quantities, and Prices directly from documents without AI or external APIs.
* **Smart Comparison:** Automatically pairs Invoices and Packing Lists by PO Number.
* **Intelligent File Management:** 
  * Audited PDFs are automatically moved to the `processed/` folder.
  * Incomplete POs (e.g., missing a packing list) remain safely in the `input/` folder as pending.
* **Excel Reporting:** Generates a comprehensive, color-coded `.xlsx` report (`openpyxl`) detailing matches, discrepancies, amounts at risk, and pre-written supplier emails.
* **Desktop UI:** A lightweight, user-friendly Electron frontend to trigger audits and open reports with one click.

## 📂 Project Structure
* `app/`: Electron frontend (UI, Main Process, Preload).
* `engine/`: Python backend engine.
  * `extract.py`: Reads PDF text and tables.
  * `compare.py`: Reconciles data and calculates statuses/risks.
  * `report.py`: Orchestrates the run, handles file moving, and generates Excel reports.
* `input/`: **Place your new Invoices and Packing Lists (.pdf) here.**
* `processed/`: Completed audits are automatically moved here. *(Ignored in git)*
* `reports/`: Generated Excel reports are saved here. *(Ignored in git)*
* `generate_samples.py`: Helper script to generate mock PDFs for testing.

## 🛠️ Prerequisites
* **Python 3+** (with `pdfplumber` and `openpyxl` installed).
* **Node.js** & **npm** (for the Electron app).

## ⚙️ Installation & Setup
1. Clone the repository.
2. Install the Electron dependencies:
   ```bash
   npm install
   ```
3. Generate sample data (optional, to test the app):
   ```bash
   py generate_samples.py
   ```
   *(Move the generated PDFs into the `input/` folder)*

## 🏃 Usage
Simply double-click the **`launch_app.bat`** file on Windows, or run:
```bash
npm start
```
1. The app window will open.
2. Click **Run Audit Now**.
3. The app will display the total POs checked and the Amount at Risk.
4. Click **Open Report** to launch the generated Excel file.
