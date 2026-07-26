from pathlib import Path

APP_TITLE = "Sales Forecasting Dashboard"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "output"

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_DATA_PATH = DATA_DIR / "sample_sales_data.csv"
MODEL_PATH = MODEL_DIR / "sales_forecasting_model.pkl"

REQUIRED_COLUMNS = ["Date", "Product", "Category", "Sales", "Quantity", "Price"]

FEATURE_COLUMNS = [
    "Day",
    "Month",
    "Year",
    "DayOfWeek",
    "DayOfYear",
    "WeekOfYear",
    "Quarter",
    "IsWeekend",
]

CURRENCY = "₹"
