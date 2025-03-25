import pandas as pd
import re
import numpy as np

def extract_max_values_from_notes_USC(input_excel: str, output_excel: str):
    """
    Function to extract Tmax (Highest IOP) values, NTG/LTG labels, and additional IOP values from clinical notes,
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

        # Define regex patterns
        tmax_pattern = r'(Highest IOP|Max Pressure|IOP Max|Pretreatment IOP up to|IOP as high as|Max IOP|IOP max on no drops|Tmax)\D{0,20}?(\d+)(?:[^\d]{0,10}(\d+))?'
        ntg_pattern = r'\b(?:ntg|ltg|normal tension|low tension)\b'
        additional_iop_pattern = r'Risk factors:\s*IOP\((\d+)\s*/\s*(\d+)\)[),]'

        # Extract Tmax values
        df_tmax = df['clinical_notes'].str.extract(tmax_pattern, flags=re.IGNORECASE)
        df_tmax.columns = ['Term', 'OD_Tmax_Note', 'OS_Tmax_Note']

        # Extract NTG/LTG label
        df['label_ntg'] = df['clinical_notes'].str.contains(ntg_pattern, flags=re.IGNORECASE, na=False).astype(int)

        # Extract additional IOP values
        additional_iop = df['clinical_notes'].str.extract(additional_iop_pattern, flags=re.IGNORECASE)
        additional_iop.columns = ['IOP_OD', 'IOP_OS']  # OD = right eye, OS = left eye

        # Combine extracted data into a single DataFrame
        combined_df = pd.DataFrame({
            'patient_ID': df['patient_ID'],
            'OD_Tmax_Note': pd.to_numeric(df_tmax['OD_Tmax_Note'], errors='coerce'),
            'OS_Tmax_Note': pd.to_numeric(df_tmax['OS_Tmax_Note'], errors='coerce'),
            'label_ntg': df['label_ntg'],
            'IOP_OD': pd.to_numeric(additional_iop['IOP_OD'], errors='coerce'),
            'IOP_OS': pd.to_numeric(additional_iop['IOP_OS'], errors='coerce')
        })

        # Replace invalid Tmax & IOP values (>100) with NaN
        combined_df.loc[combined_df['OD_Tmax_Note'] > 100, 'OD_Tmax_Note'] = np.nan
        combined_df.loc[combined_df['OS_Tmax_Note'] > 100, 'OS_Tmax_Note'] = np.nan
        combined_df.loc[combined_df['IOP_OD'] > 100, 'OD_Tmax_Note'] = np.nan
        combined_df.loc[combined_df['IOP_OS'] > 100, 'OS_Tmax_Note'] = np.nan

        # Single aggregation per patient_ID
        df_output = combined_df.groupby('patient_ID', as_index=False).agg({
            'OD_Tmax_Note': 'max',
            'OS_Tmax_Note': 'max',
            'label_ntg': 'max',
            'IOP_OD': 'max',
            'IOP_OS': 'max'
        })

        # Save to Excel
        df_output.to_excel(output_excel, index=False)

        print(f"Extraction completed. Results saved to {output_excel}")
        return df_output

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract Tmax (IOP) values, additional IOP values, and NTG labels from clinical notes.")
    parser.add_argument("input_excel", help="Path to input Excel file")
    parser.add_argument("output_excel", help="Path to output Excel file")
    args = parser.parse_args()

    extract_max_values_from_notes_USC(args.input_excel, args.output_excel)

