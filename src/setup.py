from pathlib import Path
import pandas as pd
import pyreadstat
import sys


def ensure_project_root():
    """
    Returns the project root directory (folder containing /src and /data)
    """
    current = Path(__file__).resolve()
    # Find the parent directory that contains 'src' and 'data'
    for parent in current.parents:
        if (parent / "src").exists() and (parent / "data").exists():
            root = parent
            break
    else:
        root = current.parents[1]
    sys.path.insert(0, str(root))
    return root


def load_file(filename, root=None):
    """
    Loads CSV, Excel, or Stata file by name from /data inside the project root
    """
    root = root or get_project_root()
    data_dir = root / "data"
    path = data_dir / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path)
    elif ext in (".xls", ".xlsx"):
        return pd.read_excel(path)
    elif ext == ".dta":
        return pd.read_stata(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_dta_with_col(filename: str, columns: list[str], root: Path = None):
    """
    Loads a Stata file (.dta) using pyreadstat, specifying which columns to load
    Returns (DataFrame, metadata)
    """
    root = root or ensure_project_root()
    data_dir = root / "data"
    path = data_dir / filename

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    if path.suffix.lower() != ".dta":
        raise ValueError(f"File must be a Stata file (.dta): {path}")

    df, meta = pyreadstat.read_dta(path, usecols=columns)
    return df, meta
















        
