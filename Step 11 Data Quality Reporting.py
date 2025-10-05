def generate_quality_report(original_count, cleaned_count, brand_purchase_df, brand_analysis):
    """Comprehensive data quality assessment"""
    quality_report = {
        'Metric': [
            'Total Records (Original)',
            'Valid Records (After Cleaning)',
            'Data Quality Score (%)',
            'Total Purchase Amount',
            'Average Purchase Amount',
            'Median Purchase Amount',
            'Unique Outlets',
            'Unique Brands',
            'Unique Centers',
            'Records Removed (Invalid Data)',
            'Market Concentration (HHI)'
        ],
        'Count/Value': [
            original_count,
            cleaned_count,
            f"{(cleaned_count/original_count)*100:.2f}%",
            f"₹{brand_purchase_df['Cleaned Amount'].sum():,.2f}",
            f"₹{brand_purchase_df['Cleaned Amount'].mean():,.2f}",
            f"₹{brand_purchase_df['Cleaned Amount'].median():,.2f}",
            brand_purchase_df['Outlet ID'].nunique(),
            brand_purchase_df['Brand Name'].nunique(),
            brand_purchase_df['Center'].nunique(),
            original_count - cleaned_count,
            f"{hhi_index:.0f}"
        ]
    }
    
    return pd.DataFrame(quality_report)

quality_report = generate_quality_report(
    original_count, len(brand_purchase_df), brand_purchase_df, brand_analysis
)