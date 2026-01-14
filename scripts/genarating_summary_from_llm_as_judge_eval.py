import pandas as pd
import glob

# Search all graded files in a folder
files = glob.glob("graded_*.csv")
dfs = []

print(f"Found {len(files)} graded files processing...")

for filename in files:
    try:
        # Uploading the file
        df = pd.read_csv(filename)

        # Verify that the model name exists (if not, extract from the file name)
        if 'Model_Name' not in df.columns:
            # Assume the file name is in the format graded_ModelName.csv
            model_name = filename.replace("graded_", "").replace(".csv", "")
            df['Model_Name'] = model_name

        dfs.append(df)
    except Exception as e:
        print(f"Skipping {filename}: {e}")

if dfs:
    # Consolidate all files into one table
    full_df = pd.concat(dfs, ignore_index=True)

    # Full column definition (including detailed metrics)
    target_columns = [
        # Metadata
        'Model_Name',
        'Niche',
        'Attack_Approach',
        'Prompt_Template',
        'Textual_Variation',

        # The Core Metrics
        'Final_ASR',  # (0 or 1)
        'Regex_Detected',  # Regex? (True/False)
        'LLM_ASR',  # is the Judge caught it? (0 או 1)
        'LLM_RQS',  # refusal quality (1-3)
        'LLM_Severity',  # Severity of the leak (1-5)

        # Explanations
        'Regex_Pattern',  # What pattern is caught?
        'LLM_Reason'  # explanation of the Judge
    ]

    # Filtering: Only take columns that actually exist in the files you created
    # (so if some are missing, the code won't crash, but it's worth making sure they're there)
    final_cols = [c for c in target_columns if c in full_df.columns]

    # Check if critical columns are missing and print a warning
    missing_cols = set(target_columns) - set(final_cols)
    if missing_cols:
        print(f"⚠️ Warning: The following columns were not found in the input files: {missing_cols}")

    # Creating the final table
    summary_df = full_df[final_cols]

    # Saving to a clean file ready for submission.
    output_filename = "final_benchmark_summary.csv"
    summary_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

    print(f"\n✅ Successfully created: {output_filename}")
    print(f"   Total Rows: {len(summary_df)}")
    print("\nPreview:")
    print(summary_df.head())

else:
    print("❌ No graded files found. Run evaluate_results.py first.")
