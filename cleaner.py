import pandas as pd
import argparse

def clean_dataset(file, drop_nulls, fill_nulls, remove_duplicates, normalize):
    df = pd.read_csv(file)
    report = {}

    report["initial_shape"] = df.shape
    report["missing_values"] = df.isnull().sum().to_dict()

    if drop_nulls:
        df.dropna(inplace=True)

    if fill_nulls:
        df.fillna(df.mean(numeric_only=True), inplace=True)

    if remove_duplicates:
        df.drop_duplicates(inplace=True)

    if normalize:
        for col in df.select_dtypes(include="number"):
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val != min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)

    report["final_shape"] = df.shape

    output_file = "cleaned_dataset.csv"
    df.to_csv(output_file, index=False)

    print("\n✅ Dataset cleaned successfully")
    print("📄 Output file:", output_file)
    print("📊 Cleaning Report:")
    for key, value in report.items():
        print(f"{key}: {value}")

def main():
    parser = argparse.ArgumentParser(description="Smart Dataset Cleaner CLI")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("--drop-nulls", action="store_true", help="Drop rows with null values")
    parser.add_argument("--fill-nulls", action="store_true", help="Fill nulls with column mean")
    parser.add_argument("--remove-duplicates", action="store_true", help="Remove duplicate rows")
    parser.add_argument("--normalize", action="store_true", help="Normalize numeric columns")

    args = parser.parse_args()

    clean_dataset(
        args.file,
        args.drop_nulls,
        args.fill_nulls,
        args.remove_duplicates,
        args.normalize
    )

if __name__ == "__main__":
    main()