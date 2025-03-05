# Extract Clinical Notes for IOP and NTG Label

## Overview
This Python script extracts **Tmax (Highest IOP) values** and **NTG/LTG labels** from clinical notes in an Excel file. It processes the data by:
- Identifying **IOP (Tmax) values** from structured and unstructured text.
- Extracting **the highest IOP per eye (OD/OS) per patient**.
- Detecting **mentions of NTG/LTG (Normal Tension Glaucoma / Low Tension Glaucoma)**.
- Saving the cleaned and structured data into a new Excel file.

## Installation
Make sure you have Python installed. Then, install dependencies:
```bash
pip install pandas numpy openpyxl
