def create_strategic_visualizations(brand_analysis, center_analysis, price_segments):
    """Generate comprehensive strategic charts"""
    charts = {}
    
    # Strategic color coding
    colors = {
        'excellent': '#2E8B57',    # Green - High performance
        'good': '#3CB371',         # Light Green - Good performance  
        'average': '#FFD700',      # Yellow - Average performance
        'poor': '#FF8C00',         # Orange - Needs attention
        'highlight': '#2E86AB'     # Blue - Key metrics
    }
    
    # 1. Market Overview Dashboard
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle('STRATEGIC MARKET ANALYSIS DASHBOARD', fontsize=16, fontweight='bold')
    
    # Top brands horizontal bar chart
    top_brands = brand_analysis.head(10)
    ax1.barh(range(len(top_brands)), top_brands['Total_Purchase'], color=colors['highlight'])
    ax1.set_yticks(range(len(top_brands)))
    ax1.set_yticklabels(top_brands.index)
    ax1.set_title('Top 10 Brands by Purchase Volume')
    
    # Market share pie chart
    market_share_data = brand_analysis.head(8)
    ax2.pie(market_share_data['Market_Share_Percent'], labels=market_share_data.index, 
            autopct='%1.1f%%')
    ax2.set_title('Market Share Distribution')
    
    # Price segments
    ax3.bar(price_segments.index.astype(str), price_segments['Total_Value'])
    ax3.set_title('Revenue by Price Segment')
    ax3.tick_params(axis='x', rotation=45)
    
    # Geographical performance
    top_centers = center_analysis.head(8)
    ax4.bar(range(len(top_centers)), top_centers['Total_Purchase'])
    ax4.set_xticks(range(len(top_centers)))
    ax4.set_xticklabels(top_centers.index, rotation=45)
    ax4.set_title('Top Centers by Performance')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    charts['strategic_overview'] = buf
    plt.close()
    
    return charts

charts = create_strategic_visualizations(brand_analysis, center_analysis, price_segments)