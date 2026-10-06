# Warehouse Automation Pro (AuditPro Local)

A desktop application that audits warehouse documents. It compares **Invoices** against **Packing Lists** to find short shipments, over shipments and missing items, and generates a colour-coded Excel report with ready-to-send supplier messages.

## 🎥 Demo
[Watch the 4-minute demo](https://youtu.be/zOZJCuLjzOU)

## 🚀 Features
* **Real PDF extraction:** Uses Python (`pdfplumber`) to read item codes, quantities and prices directly from the documents. No AI model or external API is involved.
* **Smart comparison:** Pairs invoices and packing lists by PO number and compares every item.
* **Clear statuses:** Received, Short Shipped, Over Shipped, Missing or Pending.
* **Amount at risk:** Calculates the money value of each discrepancy.
* **File management:** Audited PDFs move to `processed/`. POs still missing a packing list stay in `input/` as pending.
* **Excel report:** A colour-coded `.xlsx` with a summary, item details and supplier messages (`openpyxl`).
* **Desktop UI:** A lightweight Electron app to run the audit and open the report in one click.

## 📂 Project Structure
* `app/`: Electron frontend (UI, main process, preload)
* `engine/`: Python backend
  * `extract.py`: reads PDF text and tables
  * `compare.py`: reconciles data and calculates statuses and risk
  * `report.py`: runs the audit, moves files and builds the Excel report
* `input/`: **place new invoices and packing lists (.pdf) here**
* `processed/`: audited PDFs are moved here (ignored in git)
* `reports/`: generated Excel reports are saved here (ignored in git)
* `sample_data/` and `generate_samples.py`: fake sample PDFs for testing

## 🛠️ Prerequisites
* Python 3 with `pdfplumber`, `openpyxl` and `reportlab`
* Node.js and npm (for the Electron app)

## ⚙️ Installation
1. Clone the repository.
2. Install the Python libraries: `py -m pip install pdfplumber openpyxl reportlab`
3. Install the app dependencies: `npm install`
4. Optional: generate sample PDFs with `py generate_samples.py` and put them in `input/`.

## 🏃 Usage
Double-click `launch_app.bat` on Windows, or run `npm start`.
1. The app window opens.
2. Click **Run Audit Now**.
3. The app shows the POs checked and the amount at risk.
4. Click **Open Report** to open the Excel file.

## ⚠️ Current Limitations
* A new supplier layout may need a small adjustment(like same format) to the extraction rules.

## 🔮 Next Steps
* Optional Google Drive / Sheets integration
* Support for more supplier layouts

## 👤 Author
Shavak Parmar | AI Automation & Workflow Builder
freelancerparmar9@gmail.com | [LinkedIn](https://www.linkedin.com/in/shavakparmar-16b077344)
