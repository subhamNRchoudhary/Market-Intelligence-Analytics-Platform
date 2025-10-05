def competitive_benchmarking(brand_analysis, market_avg):
    """Benchmark brands against market averages"""
    benchmark = brand_analysis.copy()
    benchmark['Vs_Market_Avg'] = (benchmark['Avg_Purchase'] - market_avg).round(2)
    benchmark['Performance_Ratio'] = (
        benchmark['Avg_Purchase'] / market_avg
    ).round(2)
    
    # Performance categorization
    def performance_category(ratio):
        if ratio >= 2.0: return 'Excellent'
        elif ratio >= 1.5: return 'Good'
        elif ratio >= 1.0: return 'Average'
        elif ratio >= 0.5: return 'Below Average'
        else: return 'Poor'
    
    benchmark['Performance_Category'] = benchmark['Performance_Ratio'].apply(performance_category)
    
    return benchmark

market_avg = brand_purchase_df['Cleaned Amount'].mean()
competitive_benchmark = competitive_benchmarking(brand_analysis, market_avg)