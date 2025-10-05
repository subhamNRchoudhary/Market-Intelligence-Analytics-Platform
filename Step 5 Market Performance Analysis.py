def analyze_market_performance(data):
    """Comprehensive market performance metrics"""
    analysis = data.groupby('Brand Name').agg({
        'Cleaned Amount': ['count', 'sum', 'mean', 'median', 'std', 'min', 'max'],
        'Outlet ID': 'nunique',
        'Center': 'nunique',
        'Outlet Name': 'nunique'
    }).round(2)
    
    # Column renaming for clarity
    analysis.columns = [
        'Transaction_Count', 'Total_Purchase', 'Avg_Purchase', 'Median_Purchase',
        'Std_Purchase', 'Min_Purchase', 'Max_Purchase', 'Unique_Outlets', 
        'Unique_Centers', 'Unique_Locations'
    ]
    
    # Market share calculation
    total_purchase = analysis['Total_Purchase'].sum()
    analysis['Market_Share_Percent'] = (
        analysis['Total_Purchase'] / total_purchase * 100
    ).round(2)
    
    return analysis.sort_values('Total_Purchase', ascending=False)

brand_analysis = analyze_market_performance(brand_purchase_df)