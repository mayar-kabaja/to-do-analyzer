import pandas as pd
from pathlib import Path

# Paths relative to this script so it works from any working directory
DATA_DIR = Path(__file__).parent / "data"
df = pd.read_csv(DATA_DIR / "raw_tasks.csv")

df["text"] = df["text"].astype(str).str.strip()

df = df[df["text"].str.len() > 0]

df["priority"] = df["priority"].str.strip().str.lower()
df["category"] = df["category"].str.strip()

df.to_csv(DATA_DIR / "cleaned_tasks.csv", index=False)
print(f"Saved {len(df)} rows to {DATA_DIR / 'cleaned_tasks.csv'}")