import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PDFDataPreparer:
    """Handles PDF data preparation and formatting"""
    
    @staticmethod
    def prepare_pdf_data(dataset, analysis, chart_config=None):
        """Prepare data structure for PDF generation"""
        # Optimize: use preview_data instead of multiple .head(50) calls
        preview_data = dataset.head(50)
        
        pdf_data = {
            'filename': analysis.get('filename', ''),
            'summary': analysis['summary'],
            'missing_total': analysis['missing_values']['total'],
            'missing_by_column': analysis['missing_values']['by_column'],
            'rows_with_missing': analysis['rows_with_missing'],
            'final_data': preview_data.to_dict('records'),
            'numeric_stats': analysis['numeric_stats'],
            'categorical_freqs': analysis['categorical_freqs']
        }
        
        # Handle NaN values for charts
        improved_data = []
        for idx, row in preview_data.iterrows():
            row_dict = {}
            for col in dataset.columns:
                value = row[col]
                row_dict[col] = None if pd.isna(value) else value
            improved_data.append(row_dict)
        
        pdf_data['final_data'] = improved_data
        
        # Configure custom chart
        logger.info(f"Chart config received: {chart_config}")
        if chart_config and chart_config.get('type') and chart_config.get('xColumn') and chart_config.get('yColumn'):
            chart_type = chart_config.get('type')
            x_col = chart_config.get('xColumn')
            y_col = chart_config.get('yColumn')
            labels = chart_config.get('labels', [])
            data = chart_config.get('data', [])
            
            logger.info(f"Processing chart: type={chart_type}, x_col={x_col}, y_col={y_col}, labels_count={len(labels)}, data_count={len(data)}")
            
            if x_col in dataset.columns and y_col in dataset.columns and labels and data:
                logger.info(f"Creating chart with valid data: x_col={x_col}, y_col={y_col}")
                if chart_type == 'bar':
                    pdf_data['custom_chart'] = {
                        'type': 'bars',
                        'categories': labels,
                        'values': data,
                        'title': f'{y_col} by {x_col}'
                    }
                    logger.info(f"Bar chart created with {len(labels)} categories and {len(data)} values")
                elif chart_type == 'scatter':
                    pdf_data['custom_chart'] = {
                        'type': 'scatter',
                        'x_data': labels,
                        'y_data': data,
                        'x_label': x_col,
                        'y_label': y_col,
                        'title': f'Relationship between {x_col} and {y_col}'
                    }
                    logger.info(f"Scatter chart created with {len(labels)} x-values and {len(data)} y-values")
                elif chart_type == 'line':
                    pdf_data['custom_chart'] = {
                        'type': 'line',
                        'x_data': labels,
                        'y_data': data,
                        'x_label': x_col,
                        'y_label': y_col,
                        'title': f'{y_col} evolution by {x_col}'
                    }
                    logger.info(f"Line chart created with {len(labels)} x-values and {len(data)} y-values")
        
        # Fallback to default chart
        if 'custom_chart' not in pdf_data and 'Name' in dataset.columns and 'Income' in dataset.columns:
            logger.info("Using fallback chart with Name and Income columns")
            valid_data = dataset[['Name', 'Income']].dropna()
            if len(valid_data) > 0:
                numeric_values = pd.to_numeric(valid_data['Income'], errors='coerce')
                final_data = valid_data[numeric_values.notna()]
                if len(final_data) > 0:
                    pdf_data['custom_chart'] = {
                        'type': 'bars',
                        'categories': final_data['Name'].tolist(),
                        'values': final_data['Income'].tolist(),
                        'title': 'Income by Person'
                    }
                    logger.info(f"Fallback chart created with {len(final_data)} data points")
        elif 'custom_chart' not in pdf_data:
            logger.warning("No custom chart data available and no fallback columns found")
        
        logger.info(f"PDF data prepared for {analysis.get('filename', 'unknown file')}")
        return pdf_data 