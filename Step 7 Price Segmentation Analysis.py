def analyze_price_segments(data):
    """Segment market by purchase amount categories"""
    data['Purchase_Amount_Category'] = pd.cut(
        data['Cleaned Amount'],
        bins=[0, 1000, 5000, 10000, 50000, float('inf')],
        labels=['0-1K', '1K-5K', '5K-10K', '10K-50K', '50K+']
    )
    
    segments = data.groupby('Purchase_Amount_Category').agg({
        'Cleaned Amount': ['count', 'sum', 'mean'],
        'Outlet ID': 'nunique',
        'Brand Name': 'nunique'
    }).round(2)
    
    segments.columns = ['Transaction_Count', 'Total_Value', 'Avg_Value', 
                       'Unique_Outlets', 'Unique_Brands']
    
    total_value = segments['Total_Value'].sum()
    segments['Value_Share_Percent'] = (segments['Total_Value'] / total_value * 100).round(2)
    
    return segments

price_segments = analyze_price_segments(brand_purchase_df)