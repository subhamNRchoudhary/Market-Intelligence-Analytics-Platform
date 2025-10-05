def calculate_market_concentration(analysis_df):
    """Calculate Herfindahl-Hirschman Index and market segmentation"""
    market_shares = analysis_df['Market_Share_Percent'] / 100
    hhi_index = (market_shares ** 2).sum() * 10000
    
    # Market segmentation
    def categorize_brand_size(market_share):
        if market_share >= 10: return 'Market Leader'
        elif market_share >= 5: return 'Major Player'
        elif market_share >= 1: return 'Medium Player'
        else: return 'Small Player'
    
    analysis_df['Brand_Size_Category'] = analysis_df['Market_Share_Percent'].apply(categorize_brand_size)
    
    return hhi_index, analysis_df

hhi_index, brand_analysis = calculate_market_concentration(brand_analysis)