# Market-Intelligence-Analytics-Platform
A comprehensive data analysis and visualization platform for market research and business intelligence. This project demonstrates advanced data processing, statistical analysis, and strategic insights generation capabilities.


## Project Overview

This platform processes market research data to generate actionable business intelligence through automated data cleaning, statistical analysis, and strategic visualization. It transforms raw survey data into professional reports with clear strategic recommendations.

## Features

- **Automated Data Processing**: Cleans and transforms raw market research data
- **Statistical Analysis**: Comprehensive market concentration and performance metrics
- **Strategic Visualization**: Professional charts with clear action indicators
- **Quality Assessment**: Data reliability scoring and validation
- **Multi-dimensional Analysis**: Brand performance, geographical analysis, price segmentation
- **Executive Reporting**: Automated report generation with strategic insights

## Technical Architecture

### Step 1: Environment Setup and Dependencies
```python
import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import io
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Professional visualization settings
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
```

### Step 2: Configuration and File Management
```python
# Project directory structure
cleaning_dir = r"../data/processed"
analysis_output_dir = r"../reports"

# Create output directories
os.makedirs(analysis_output_dir, exist_ok=True)

# Dynamic file naming with timestamps
today_date = datetime.now().strftime("%Y-%m-%d")
analysis_file_name = f"Market_Analysis_Report_{today_date}.xlsx"
analysis_file_path = os.path.join(analysis_output_dir, analysis_file_name)
```

### Step 3: Data Loading and Validation
```python
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
```

### Step 4: Data Quality Enhancement
```python
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
```

### Step 5: Market Performance Analysis
```python
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
```

### Step 6: Market Concentration Metrics
```python
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
```

### Step 7: Price Segmentation Analysis
```python
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
```

### Step 8: Geographical Performance Analysis
```python
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
```

### Step 9: Strategic Visualization System
```python
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
```

### Step 10: Competitive Benchmarking
```python
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
```

### Step 11: Data Quality Reporting
```python
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
```

### Step 12: Professional Excel Reporting
```python
def create_professional_report(analysis_data, charts, output_path):
    """Generate professional Excel report with styling"""
    wb = Workbook()
    wb.remove(wb.active)
    
    # Add all analysis sheets
    analyses = [
        ('Brand_Performance', brand_analysis),
        ('Market_Concentration', market_segments),
        ('Price_Segmentation', price_segments),
        ('Geographical_Analysis', center_analysis),
        ('Competitive_Benchmarking', competitive_benchmark),
        ('Data_Quality_Report', quality_report)
    ]
    
    for sheet_name, data in analyses:
        if isinstance(data, pd.DataFrame) and not data.empty:
            ws = wb.create_sheet(sheet_name)
            for row in dataframe_to_rows(data, index=True, header=True):
                ws.append(row)
    
    # Apply professional styling
    apply_excel_styling(wb)
    
    # Add charts
    if 'strategic_overview' in charts:
        ws = wb['Brand_Performance']
        img = Image(charts['strategic_overview'])
        img.anchor = 'K2'
        ws.add_image(img)
    
    wb.save(output_path)
    return output_path

report_path = create_professional_report(
    {'brand_analysis': brand_analysis, 'center_analysis': center_analysis},
    charts, analysis_file_path
)
```

### Step 13: Strategic Insights Generation
```python
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
```

### Step 14: Project Summary and Output
```python
def project_summary(report_path, analyses_performed):
    """Generate project completion summary"""
    print("\n" + "="*60)
    print("PROJECT EXECUTION SUMMARY")
    print("="*60)
    print(f"✅ Analysis completed successfully!")
    print(f"📁 Report saved: {report_path}")
    print(f"📊 Analyses performed: {len(analyses_performed)}")
    print(f"📈 Market metrics calculated: HHI, Market Share, Performance Ratios")
    print(f"🎨 Professional visualizations: Strategic charts with color coding")
    print(f"📋 Quality assessment: Comprehensive data validation")
    print(f"💡 Strategic insights: Actionable business recommendations")
    
    return {
        'report_path': report_path,
        'analyses_count': len(analyses_performed),
        'completion_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

analyses_performed = [
    'Market Performance', 'Concentration Analysis', 'Price Segmentation',
    'Geographical Analysis', 'Competitive Benchmarking', 'Quality Assessment'
]

summary = project_summary(analysis_file_path, analyses_performed)
```

## Installation and Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/market-intelligence-platform.git
cd market-intelligence-platform
```

2. **Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn openpyxl scipy
```

3. **Prepare your data**
   - Place your input data in the `data/raw/` directory
   - Ensure data follows the expected format

4. **Run the analysis**
```python
python market_analysis_platform.py
```

## Project Structure
```
market-intelligence-platform/
├── data/
│   ├── raw/           # Input data files
│   └── processed/     # Cleaned data files
├── reports/           # Generated analysis reports
├── src/
│   ├── analysis.py    # Core analysis functions
│   ├── visualization.py # Chart generation
│   └── reporting.py   # Report generation
└── README.md
```

## Key Features Demonstrated

- **Data Processing**: Automated cleaning and validation pipelines
- **Statistical Analysis**: Market concentration, performance metrics, segmentation
- **Visualization**: Professional charts with strategic color coding
- **Reporting**: Automated Excel report generation with styling
- **Quality Control**: Comprehensive data validation and reliability scoring
- **Strategic Insights**: Actionable business intelligence generation

## Technologies Used

- **Pandas & NumPy**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Data visualization
- **OpenPyXL**: Excel report generation
- **SciPy**: Statistical analysis
- **Python Standard Library**: File handling and utilities

This project demonstrates advanced data analysis capabilities suitable for market research, business intelligence, and strategic planning applications.
