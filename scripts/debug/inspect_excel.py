import pandas as pd

def inspect_excel():
    file_path = "Gameweek 4 UCL 25:26 Points.xlsx"
    try:
        df = pd.read_excel(file_path)
        print("Columns:", df.columns.tolist())
        
        targets = ["Ryerson", "Svensson"]
        for t in targets:
            # Fuzzy match
            row = df[df['name'].astype(str).str.contains(t, case=False)]
            if not row.empty:
                print(f"\nFound {t} in Excel:")
                print(row.to_string())
            else:
                print(f"\n{t} NOT FOUND in Excel.")

    except Exception as e:
        print(f"Error reading excel: {e}")

if __name__ == "__main__":
    inspect_excel()
