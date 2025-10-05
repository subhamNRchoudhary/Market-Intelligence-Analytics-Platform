def enhance_data_quality(df):
    """Apply comprehensive data cleaning and validation"""
    # Convert amounts to numeric
    df['Cleaned Amount'] = pd.to_numeric(df['Cleaned Amount'], errors='coerce')
    
    # Remove invalid records
    original_count = len(df)
    df = df.dropna(subset=['Cleaned Amount'])
    df = df[df['Cleaned Amount'] > 0]
    cleaned_count = len(df)
    
    # Standardize text fields
    text_columns = ['Brand Name', 'Center', 'Outlet Name', 'Phone Number']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
    
    print(f"Data quality: {cleaned_count}/{original_count} records retained "
          f"({(cleaned_count/original_count)*100:.1f}%)")
    return df

brand_purchase_df = enhance_data_quality(brand_purchase_df)