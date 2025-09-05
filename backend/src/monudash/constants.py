import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent.parent.parent

# Application directories
STATIC_DIR = Path(os.getenv('STATIC_DIR', BASE_DIR / "static"))
RESOURCES_DIR = Path(os.getenv('RESOURCES_DIR', PROJECT_ROOT / "resources"))

#link to the static directory
if not STATIC_DIR.exists():
    STATIC_DIR.symlink_to(PROJECT_ROOT / "frontend" / "dist", target_is_directory=True)

# API Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000

# Data files
MONUMENTS_ORIG_CSV = RESOURCES_DIR / "denkmal_prodenkmal_csv.csv"
MONUMENTS_CSV = RESOURCES_DIR / "monuments_with_coordinates.csv"
DATABASE_FILE = RESOURCES_DIR / "monuments.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{DATABASE_FILE}")

if __name__ == "__main__":
    # Print all local variables
    local_vars = locals()
    print("All local variables:")
    for var_name, var_value in list(local_vars.items()):
        print(f"  {var_name}: {var_value}")