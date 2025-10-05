# Project directory structure
cleaning_dir = r"../data/processed"
analysis_output_dir = r"../reports"

# Create output directories
os.makedirs(analysis_output_dir, exist_ok=True)

# Dynamic file naming with timestamps
today_date = datetime.now().strftime("%Y-%m-%d")
analysis_file_name = f"Market_Analysis_Report_{today_date}.xlsx"
analysis_file_path = os.path.join(analysis_output_dir, analysis_file_name)