import csv
import os
import json
import subprocess


def load_config():
    """Loads the configuration from config.json and returns it as a dictionary."""
    # Get the absolute path of the current directory where conftest.py is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct the correct path for config.json (move up one level if necessary)
    CONFIG_PATH = os.path.join(BASE_DIR, "../config/config.json")

    print(f"DEBUG: Looking for config.json at {CONFIG_PATH}")

    # Load the configuration from config.json
    try:
        with open(CONFIG_PATH, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"ERROR: Could not find config.json {CONFIG_PATH}") from e
    
def read_data_from_csv(file_path):
     """Reads  data from a CSV file. """
     data = []
     with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
     return data


def read_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def run_k6_test(js_file_path, vus=20, test_type="FIXED"):
    summary_file = "summary.json"
    
    # 1. ניקוי קבצים ישנים
    if os.path.exists(summary_file):
        try:
            os.remove(summary_file)
        except:
            pass

    # 2. בניית הפקודה
    command = [
        "k6", "run",
        "--env", f"TEST_TYPE={test_type}",
        "--env", f"USERS={vus}",
        "--summary-export", summary_file,
        js_file_path
    ]
    
    print(f"\n🚀 מריץ בדיקת עומסים: {test_type}...")

    try:
        # 3. הרצה - הוספנו shell=True שזה קריטי בווינדוס כדי לזהות את k6
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        # הדפסת הפלט של k6 כדי שתוכל לראות את האחוזים רצים
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # 4. בדיקת קריסה (Threshold breached)
        # ב-k6, קוד 97 אומר שהבדיקה נעצרה בגלל עומס יתר
        if result.returncode != 0:
            print("\n" + "!"*40)
            print(f"💥 ALERT: SYSTEM CRASHED (Code: {result.returncode}) 💥")
            print("!"*40)
            return 1.0  # מחזירים 100% כישלון

        # 5. קריאת נתונים מהקובץ
        if os.path.exists(summary_file):
            with open(summary_file, 'r') as f:
                data = json.load(f)
            metrics = data.get("metrics", {})
            rate = metrics.get("http_req_failed", {}).get("values", {}).get("rate", 0.0)
            return float(rate)

    except Exception as e:
        print(f"❌ שגיאה בהרצת k6: {e}")
        return 1.0
            
    return 0.0