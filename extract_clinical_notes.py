import pandas as pd
import re
import numpy as np

def extract_max_values_from_notes(input_excel: str, output_excel: str):
    """
    Function to extract Tmax (Highest IOP) values and NTG/LTG labels from clinical notes,
    and aggregate the highest IOP values per patient_ID.

    Parameters:
    input_excel (str): Path to input Excel file with columns 'patient_ID' and 'clinical_notes'.
    output_excel (str): Path to output Excel file with aggregated values per patient.
    """

    try:
        # Load Excel file
        df = pd.read_excel(input_excel)

        # Ensure required columns exist
        if 'patient_ID' not in df.columns or 'clinical_notes' not in df.columns:
            raise ValueError("Missing required columns: 'patient_ID' and 'clinical_notes'")

        # Define regex pattern for Tmax values (Highest IOP)
        tmax_pattern = r'(Highest IOP|Max Pressure|IOP Max|Pretreatment IOP up to|IOP as high as|Max IOP|IOP max on no drops|Tmax)\D{0,20}?(\d+)(?:[^\d]{0,10}(\d+))?'

        # Extract Tmax values
        df_tmax = df['clinical_notes'].str.extract(tmax_pattern, flags=re.IGNORECASE)
        df_tmax.columns = ['Term', 'OD_Tmax_Note', 'OS_Tmax_Note']

        # Convert extracted values to float
        df_tmax['OD_Tmax_Note'] = pd.to_numeric(df_tmax['OD_Tmax_Note'], errors='coerce')
        df_tmax['OS_Tmax_Note'] = pd.to_numeric(df_tmax['OS_Tmax_Note'], errors='coerce')

        # Replace invalid values (greater than 100) with NaN
        df_tmax.loc[df_tmax['OD_Tmax_Note'] > 100, 'OD_Tmax_Note'] = np.nan
        df_tmax.loc[df_tmax['OS_Tmax_Note'] > 100, 'OS_Tmax_Note'] = np.nan

        # Attach patient_ID for aggregation
        df_tmax['patient_ID'] = df['patient_ID']

        # Aggregate to get max IOP per patient
        df_tmax_max = df_tmax.groupby('patient_ID')[['OD_Tmax_Note', 'OS_Tmax_Note']].max().reset_index()

        # Define regex pattern for NTG/LTG labels
        #ntg_pattern = r'\b(ntg|ltg|normal tension|low tension)\b'
        ntg_pattern = r'\b(?:ntg|ltg|normal tension|low tension)\b'  # Non-capturing group

        # Extract NTG/LTG label presence as binary at the patient level (any mention in notes)
        df['label_ntg'] = df['clinical_notes'].str.contains(ntg_pattern, flags=re.IGNORECASE, na=False).astype(int)

        # Aggregate NTG label at the patient level (if mentioned anywhere in notes, set to 1)
        df_ntg_label = df.groupby('patient_ID')['label_ntg'].max().reset_index()

        # Merge extracted values with patient_ID
        df_output = df_tmax_max.merge(df_ntg_label, on='patient_ID', how='left')

        # Save to Excel
        df_output.to_excel(output_excel, index=False)
        
        print(f"Extraction completed. Results saved to {output_excel}")
        return df_output

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract Tmax (IOP) values and NTG labels from clinical notes.")
    parser.add_argument("input_excel", help="Path to input Excel file")
    parser.add_argument("output_excel", help="Path to output Excel file")
    args = parser.parse_args()
    
    extract_max_values_from_notes(args.input_excel, args.output_excel)