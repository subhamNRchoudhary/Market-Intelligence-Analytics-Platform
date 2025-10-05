def load_latest_dataset(cleaning_dir):
    """Load the most recent processed dataset"""
    excel_files = [f for f in os.listdir(cleaning_dir) 
                   if f.startswith('Cleaned_Data_') and f.endswith('.xlsx')]
    
    if not excel_files:
        raise FileNotFoundError("No processed data files found")
    
    # Get most recent file
    latest_file = max(excel_files, 
                     key=lambda x: datetime.strptime(x.split('_')[-1].split('.')[0], "%Y-%m-%d"))
    input_file_path = os.path.join(cleaning_dir, latest_file)
    
    print(f"Loading data from: {latest_file}")
    return input_file_path

# Load datasets
input_file_path = load_latest_dataset(cleaning_dir)
brand_purchase_df = pd.read_excel(input_file_path, sheet_name='Brand_Purchase')
monthly_sell_df = pd.read_excel(input_file_path, sheet_name='Monthly_Sell')