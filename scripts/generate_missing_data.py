"""
Generate datasets with missing values for MICE imputation demonstration
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def introduce_missing_values(df, column, missing_percentage=0.20):
    """
    Randomly introduce missing values in a specific column

    Args:
        df: DataFrame
        column: Column name to introduce missing values
        missing_percentage: Percentage of values to set as missing (default 20%)

    Returns:
        DataFrame with missing values
    """
    df_copy = df.copy()
    n_missing = int(len(df_copy) * missing_percentage)
    missing_indices = np.random.choice(df_copy.index, size=n_missing, replace=False)
    df_copy.loc[missing_indices, column] = np.nan
    return df_copy

def main():
    # Define paths
    data_dir = Path(__file__).parent.parent / 'data'
    original_file = data_dir / 'Global_Cybersecurity_Threats_2015-2024.csv'
    output_file = data_dir / 'global_threat_landscape_with_missing.csv'

    print("=" * 80)
    print("GENERATING DATASET WITH MISSING VALUES")
    print("=" * 80)

    # Load original dataset
    print(f"\n1. Loading original dataset from: {original_file}")
    df = pd.read_csv(original_file)
    print(f"   [OK] Loaded {len(df):,} records with {len(df.columns)} columns")

    # Check current missing values
    original_missing = df['Financial Loss (in Million $)'].isnull().sum()
    print(f"   [OK] Original missing values in Financial Loss: {original_missing}")

    # Introduce missing values in Financial Loss column
    print(f"\n2. Introducing 20% missing values in 'Financial Loss (in Million $)'")
    df_with_missing = introduce_missing_values(df, 'Financial Loss (in Million $)', 0.20)

    new_missing = df_with_missing['Financial Loss (in Million $)'].isnull().sum()
    missing_pct = (new_missing / len(df_with_missing)) * 100

    print(f"   [OK] Missing values introduced: {new_missing} ({missing_pct:.2f}%)")

    # Save to CSV
    print(f"\n3. Saving dataset with missing values to: {output_file}")
    df_with_missing.to_csv(output_file, index=False)
    print(f"   [OK] Dataset saved successfully!")

    # Display statistics
    print(f"\n" + "=" * 80)
    print("DATASET STATISTICS")
    print("=" * 80)
    print(f"\nOriginal Dataset:")
    print(f"  - Total records: {len(df):,}")
    print(f"  - Financial Loss - Missing: {original_missing} ({original_missing/len(df)*100:.2f}%)")
    print(f"  - Financial Loss - Mean: ${df['Financial Loss (in Million $)'].mean():.2f}M")
    print(f"  - Financial Loss - Median: ${df['Financial Loss (in Million $)'].median():.2f}M")

    print(f"\nDataset with Missing Values:")
    print(f"  - Total records: {len(df_with_missing):,}")
    print(f"  - Financial Loss - Missing: {new_missing} ({missing_pct:.2f}%)")

    valid_values = df_with_missing['Financial Loss (in Million $)'].dropna()
    print(f"  - Financial Loss - Mean: ${valid_values.mean():.2f}M")
    print(f"  - Financial Loss - Median: ${valid_values.median():.2f}M")

    print(f"\n" + "=" * 80)
    print("[SUCCESS] Dataset generation complete!")
    print(f"[SUCCESS] Output file: {output_file}")
    print("=" * 80)

    return df_with_missing

if __name__ == "__main__":
    main()
