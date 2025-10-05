def analyze_geographical_performance(data):
    """Center-wise performance analysis"""
    center_analysis = data.groupby('Center').agg({
        'Cleaned Amount': ['sum', 'mean', 'count', 'std', 'median'],
        'Outlet ID': 'nunique',
        'Brand Name': 'nunique',
        'Outlet Name': 'nunique'
    }).round(2)
    
    center_analysis.columns = [
        'Total_Purchase', 'Avg_Purchase', 'Transaction_Count', 'Std_Purchase', 
        'Median_Purchase', 'Unique_Outlets', 'Unique_Brands', 'Unique_Locations'
    ]
    
    total_purchase = center_analysis['Total_Purchase'].sum()
    center_analysis['Market_Share_Percent'] = (
        center_analysis['Total_Purchase'] / total_purchase * 100
    ).round(2)
    
    return center_analysis.sort_values('Total_Purchase', ascending=False)

center_analysis = analyze_geographical_performance(brand_purchase_df)