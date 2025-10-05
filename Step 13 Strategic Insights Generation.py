def generate_strategic_insights(brand_analysis, hhi_index, quality_report):
    """Generate actionable business insights"""
    insights = []
    
    # Market Structure Insights
    market_leaders = brand_analysis[brand_analysis['Market_Share_Percent'] >= 10]
    insights.append(f"🏢 MARKET STRUCTURE:")
    insights.append(f"• Market Concentration: HHI = {hhi_index:.0f} "
                   f"({'Highly Concentrated' if hhi_index > 2500 else 'Competitive'})")
    insights.append(f"• Market Leaders: {len(market_leaders)} brands with ≥10% share")
    
    # Performance Insights
    top_brand = brand_analysis.index[0]
    top_brand_share = brand_analysis.iloc[0]['Market_Share_Percent']
    insights.append(f"🎯 PERFORMANCE LEADERS:")
    insights.append(f"• Market Leader: {top_brand} ({top_brand_share}% market share)")
    
    # Strategic Recommendations
    insights.append(f"💡 STRATEGIC RECOMMENDATIONS:")
    if hhi_index > 2500:
        insights.append("• Focus on competitor analysis and market entry barriers")
        insights.append("• Explore niche markets and underserved segments")
    else:
        insights.append("• Emphasize differentiation and brand building")
        insights.append("• Consider partnership strategies")
    
    return "\n".join(insights)

strategic_insights = generate_strategic_insights(brand_analysis, hhi_index, quality_report)
print(strategic_insights)