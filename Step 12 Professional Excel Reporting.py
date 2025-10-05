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