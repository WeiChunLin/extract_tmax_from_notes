# Extract Clinical Notes for IOP and NTG Label

## Overview

This Python script extracts **Tmax (Highest IOP) values** and **NTG/LTG labels** from clinical notes in an Excel file. It processes the data by:

- Identifying **IOP (Tmax) values** from structured and unstructured text.
- Extracting **the highest IOP per eye (OD/OS) per patient**.
- Detecting **mentions of NTG/LTG (Normal Tension Glaucoma / Low Tension Glaucoma)**.
- Saving the cleaned and structured data into a new Excel file.

## Usage

Run the script with:

```bash
python extract_clinical_notes.py input_data.xlsx output_data.xlsx
```

Replace `input_data.xlsx` with your **Excel file** containing `patient_ID` and `clinical_notes`.

## Output

The script generates an **Excel file** (`output_data.xlsx`) with:

- `patient_ID`: Unique patient identifier.
- `OD_Tmax_Note`: Highest IOP value for **OD (right eye)**.
- `OS_Tmax_Note`: Highest IOP value for **OS (left eye)**.
- `label_ntg`: **1 if NTG/LTG is mentioned**, otherwise **0**.

## Notes

- The script **handles missing values** and **ensures numerical accuracy**.
- It **filters out unrealistic IOP values (>100 mmHg)**.

This project is licensed under the MIT License.

