import pandas as pd
import sys
import os
import platform
from pathlib import Path

def open_file(path):
    """Open the file with the default app depending on the OS."""
    try:
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':  # macOS
            os.system(f'open "{path}"')
        else:  # Linux
            os.system(f'xdg-open "{path}"')
    except Exception as e:
        print(f"⚠️ Could not open file automatically: {e}")

def refresh_csv(file_path):
    file = Path(file_path)

    if not file.exists():
        print(f"❌ File not found: {file}")
        return

    print(f"🔄 Reloading: {file.name}")

    # Load CSV
    df = pd.read_csv(file)

    # Save new version
    refreshed_path = file.parent / f"{file.stem}_view.csv"
    df.to_csv(refreshed_path, index=False)

    print(f"✅ Reloaded and saved as: {refreshed_path}")
    print(f"📊 Rows: {len(df)}, Columns: {len(df.columns)}")
    print("💡 Opening in your default viewer...")

    # Open file
    open_file(refreshed_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/refresh_csv.py <path_to_csv>")
    else:
        refresh_csv(sys.argv[1])
