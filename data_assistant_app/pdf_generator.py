from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import io
import base64
from datetime import datetime
import os
import tempfile
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image as PILImage
import logging
from .translations import get_text

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, language='en'):
        self.language = language
        self.styles = getSampleStyleSheet()
        self._configure_styles()
    
    def _configure_styles(self):
        """Configure PDF document styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2a4d69')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#4a90e2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold'
        ))
    
    def _render_chart_to_image(self, figure, width=6*inch, height=3*inch):
        """Convert matplotlib figure to ReportLab image"""
        try:
            buffer = io.BytesIO()
            figure.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            image = RLImage(buffer, width=width, height=height)
            return image
        except Exception as e:
            logger.error(f"Chart rendering failed: {e}")
            return None
    
    def generate_pdf(self, pdf_data, output_path):
        """Generate complete PDF report"""
        logger.info(f"Starting PDF generation: {output_path}")
        
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            content_elements = []
            
            # Document structure
            content_elements.append(Paragraph(get_text('SYNAPSE_DATA_ANALYSIS_REPORT', self.language), self.styles['CustomTitle']))
            content_elements.append(Spacer(1, 20))
            
            # Executive Summary
            content_elements.extend(self._build_executive_summary(pdf_data))
            
            # Table of Contents placeholder
            content_elements.append(Paragraph(get_text('TABLE_OF_CONTENTS', self.language), self.styles['CustomSubtitle']))
            content_elements.append(Paragraph("1. " + get_text('FILE_INFORMATION', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("2. " + get_text('MISSING_VALUES', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("3. " + get_text('FINAL_DATA_TABLE', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("4. " + get_text('DESCRIPTIVE_STATISTICS', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("5. " + get_text('CUSTOM_CHART', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("6. " + get_text('DATA_QUALITY_INSIGHTS', self.language), self.styles['CustomBody']))
            content_elements.append(Paragraph("7. " + get_text('OBSERVATIONS_AND_RECOMMENDATIONS', self.language), self.styles['CustomBody']))
            content_elements.append(Spacer(1, 20))
            
            content_elements.extend(self._build_file_info_section(pdf_data))
            
            if pdf_data.get('missing_total', 0) > 0:
                content_elements.extend(self._build_missing_values_section(pdf_data))
            
            if pdf_data.get('final_data'):
                content_elements.extend(self._build_data_table_section(pdf_data))
            
            if pdf_data.get('numeric_stats'):
                content_elements.extend(self._build_statistics_section(pdf_data))
                content_elements.extend(self._build_correlation_analysis(pdf_data))
            
            if pdf_data.get('categorical_freqs'):
                content_elements.extend(self._build_frequencies_section(pdf_data))
            
            # Custom chart section
            if pdf_data.get('custom_chart'):
                logger.info("Processing custom chart")
                content_elements.extend(self._build_custom_chart_section(pdf_data))
            
            content_elements.extend(self._build_data_quality_insights(pdf_data))
            
            if pdf_data.get('cleaning_notes'):
                content_elements.extend(self._build_cleaning_notes_section(pdf_data))
            
            content_elements.extend(self._build_recommendations_section(pdf_data))
            
            logger.info(f"Building PDF with {len(content_elements)} elements")
            doc.build(content_elements)
            logger.info(f"PDF generated successfully: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise
    
    def _build_file_info_section(self, pdf_data):
        """Build file information section"""
        elements = []
        
        elements.append(Paragraph(get_text('FILE_INFORMATION', self.language), self.styles['CustomSubtitle']))
        
        file_info = [
            [get_text('FILE_NAME', self.language) + ':', pdf_data.get('filename', 'N/A')],
            [get_text('NUMBER_OF_ROWS', self.language) + ':', str(pdf_data.get('summary', {}).get('rows', 'N/A'))],
            [get_text('NUMBER_OF_COLUMNS', self.language) + ':', str(pdf_data.get('summary', {}).get('columns', 'N/A'))],
            [get_text('ANALYSIS_DATE', self.language) + ':', datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
        ]
        
        data_types = pdf_data.get('summary', {}).get('data_types', {})
        if data_types:
            for col, dtype in list(data_types.items())[:5]:
                file_info.append([get_text('TYPE_OF', self.language) + f' {col}:', str(dtype)])
            if len(data_types) > 5:
                file_info.append(['...', get_text('AND_MORE_COLUMNS', self.language, n=len(data_types) - 5)])
        
        table = Table(file_info, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_executive_summary(self, pdf_data):
        """Build executive summary section"""
        elements = []
        
        elements.append(Paragraph(get_text('EXECUTIVE_SUMMARY', self.language), self.styles['CustomSubtitle']))
        
        summary = pdf_data.get('summary', {})
        missing_total = pdf_data.get('missing_total', 0)
        total_rows = summary.get('rows', 0)
        total_cols = summary.get('columns', 0)
        
        # Calculate data quality score
        total_cells = total_rows * total_cols
        quality_score = ((total_cells - missing_total) / total_cells * 100) if total_cells > 0 else 100
        
        elements.append(Paragraph(get_text('REPORT_ANALYZES_DATASET', self.language, rows=total_rows, cols=total_cols), self.styles['CustomBody']))
        elements.append(Spacer(1, 6))
        
        if missing_total > 0:
            elements.append(Paragraph(get_text('DATA_QUALITY_SCORE', self.language, score=quality_score, missing=missing_total), self.styles['CustomBody']))
        else:
            elements.append(Paragraph(get_text('DATA_QUALITY_SCORE_NO_MISSING', self.language, score=quality_score), self.styles['CustomBody']))
        
        elements.append(Spacer(1, 6))
        
        # Key insights
        numeric_stats = pdf_data.get('numeric_stats', {})
        if numeric_stats:
            elements.append(Paragraph(get_text('KEY_INSIGHTS', self.language), self.styles['CustomBody']))
            elements.append(Spacer(1, 6))
            
            for col, stats in list(numeric_stats.items())[:3]:  # Show top 3 columns
                mean_val = stats.get('mean', 0)
                std_val = stats.get('std', 0)
                elements.append(Paragraph(get_text('COLUMN_STATS', self.language, col=col, mean=mean_val, std=std_val), self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_missing_values_section(self, pdf_data):
        """Build missing values analysis section"""
        elements = []
        
        elements.append(Paragraph(get_text('MISSING_VALUES', self.language), self.styles['CustomSubtitle']))
        
        missing_total = pdf_data.get('missing_total', 0)
        total_rows = pdf_data.get('summary', {}).get('rows', 0)
        total_cols = pdf_data.get('summary', {}).get('columns', 1)
        missing_percentage = (missing_total / (total_rows * total_cols)) * 100 if total_rows > 0 else 0
        
        elements.append(Paragraph(get_text('TOTAL_MISSING_VALUES', self.language, total=missing_total, percentage=missing_percentage), self.styles['CustomBody']))
        elements.append(Spacer(1, 12))
        
        missing_by_column = pdf_data.get('missing_by_column', {})
        if missing_by_column:
            table_data = [[get_text('COLUMN', self.language), get_text('MISSING_VALUES_COL', self.language), get_text('PERCENTAGE', self.language)]]
            for col, count in missing_by_column.items():
                if count > 0:
                    col_percentage = (count / total_rows) * 100 if total_rows > 0 else 0
                    table_data.append([col, str(count), f"{col_percentage:.1f}%"])
            
            if len(table_data) > 1:
                table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
        
        rows_with_missing = pdf_data.get('rows_with_missing', [])
        if rows_with_missing:
            elements.append(Paragraph(get_text('EXAMPLES_INCOMPLETE_ROWS', self.language) + ":", self.styles['CustomBody']))
            elements.append(Spacer(1, 6))
            
            for row_info in rows_with_missing[:3]:
                missing_cols = ', '.join(row_info['missing_columns'])
                elements.append(Paragraph(
                    get_text('ROW_MISSING', self.language, n=row_info['index'] + 1, cols=missing_cols), 
                    self.styles['CustomBody']
                ))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_data_table_section(self, pdf_data):
        """Build final data table section"""
        elements = []
        
        elements.append(Paragraph(get_text('FINAL_DATA_TABLE', self.language), self.styles['CustomSubtitle']))
        
        final_data = pdf_data.get('final_data', [])
        if final_data:
            rows_to_show = final_data[:10]
            
            if rows_to_show:
                columns = list(rows_to_show[0].keys())
                
                table_data = [columns]
                
                for row in rows_to_show:
                    table_data.append([str(row.get(col, '')) for col in columns])
                
                if len(final_data) > 10:
                    table_data.append(['...'] * len(columns))
                    table_data.append([f'Showing 10 of {len(final_data)} rows'] + [''] * (len(columns) - 1))
                
                col_widths = [4*inch / len(columns)] * len(columns)
                table = Table(table_data, colWidths=col_widths)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
                ]))
                elements.append(table)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_statistics_section(self, pdf_data):
        """Build descriptive statistics section"""
        elements = []
        
        elements.append(Paragraph(get_text('DESCRIPTIVE_STATISTICS', self.language), self.styles['CustomSubtitle']))
        
        numeric_stats = pdf_data.get('numeric_stats', {})
        if numeric_stats:
            table_data = [[get_text('COLUMN', self.language), get_text('MEAN', self.language), get_text('MEDIAN', self.language), get_text('STD_DEV', self.language), get_text('MIN', self.language), get_text('MAX', self.language)]]
            
            for col, stats in numeric_stats.items():
                table_data.append([
                    col,
                    f"{stats.get('mean', 0):.2f}",
                    f"{stats.get('median', 0):.2f}",
                    f"{stats.get('std', 0):.2f}",
                    f"{stats.get('min', 0):.2f}",
                    f"{stats.get('max', 0):.2f}"
                ])
            
            table = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
            ]))
            elements.append(table)
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_correlation_analysis(self, pdf_data):
        """Build correlation analysis section"""
        elements = []
        
        elements.append(Paragraph(get_text('CORRELATION_ANALYSIS', self.language), self.styles['CustomSubtitle']))
        
        numeric_stats = pdf_data.get('numeric_stats', {})
        if len(numeric_stats) >= 2:
            elements.append(Paragraph(get_text('CORRELATION_HELP', self.language), self.styles['CustomBody']))
            elements.append(Spacer(1, 6))
            
            # Get numeric columns
            numeric_cols = list(numeric_stats.keys())
            
            # Create correlation matrix (simplified)
            if len(numeric_cols) <= 5:  # Only show if we have reasonable number of columns
                table_data = [['Column'] + numeric_cols]
                
                for col1 in numeric_cols:
                    row = [col1]
                    for col2 in numeric_cols:
                        if col1 == col2:
                            row.append('1.00')
                        else:
                            # Simplified correlation (in real implementation, calculate actual correlation)
                            row.append('N/A')
                    table_data.append(row)
                
                table = Table(table_data, colWidths=[1.2*inch] + [0.8*inch] * len(numeric_cols))
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
                ]))
                elements.append(table)
                elements.append(Spacer(1, 6))
                elements.append(Paragraph(get_text('CORRELATION_NOTE', self.language), self.styles['CustomBody']))
            else:
                elements.append(Paragraph(get_text('TOO_MANY_COLUMNS', self.language, n=len(numeric_cols)), self.styles['CustomBody']))
        else:
            elements.append(Paragraph(get_text('INSUFFICIENT_COLUMNS', self.language), self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_data_quality_insights(self, pdf_data):
        """Build data quality insights section"""
        elements = []
        
        elements.append(Paragraph(get_text('DATA_QUALITY_INSIGHTS', self.language), self.styles['CustomSubtitle']))
        
        summary = pdf_data.get('summary', {})
        missing_total = pdf_data.get('missing_total', 0)
        total_rows = summary.get('rows', 0)
        total_cols = summary.get('columns', 0)
        numeric_stats = pdf_data.get('numeric_stats', {})
        categorical_freqs = pdf_data.get('categorical_freqs', {})
        
        insights = []
        
        # Data completeness
        if missing_total == 0:
            insights.append("✓ <b>Complete Data</b>: No missing values detected")
        elif missing_total / (total_rows * total_cols) < 0.05:
            insights.append("✓ <b>Good Data Quality</b>: Less than 5% missing values")
        elif missing_total / (total_rows * total_cols) < 0.15:
            insights.append("⚠ <b>Moderate Data Quality</b>: 5-15% missing values")
        else:
            insights.append("✗ <b>Poor Data Quality</b>: More than 15% missing values")
        
        # Data variety
        if numeric_stats and categorical_freqs:
            insights.append("✓ <b>Mixed Data Types</b>: Both numeric and categorical variables present")
        elif numeric_stats:
            insights.append("✓ <b>Numeric Dataset</b>: All variables are numeric")
        elif categorical_freqs:
            insights.append("✓ <b>Categorical Dataset</b>: All variables are categorical")
        
        # Data volume
        if total_rows >= 1000:
            insights.append("✓ <b>Large Dataset</b>: Sufficient data for robust analysis")
        elif total_rows >= 100:
            insights.append("✓ <b>Medium Dataset</b>: Adequate data for analysis")
        else:
            insights.append("⚠ <b>Small Dataset</b>: Limited data may affect analysis reliability")
        
        # Outlier detection (simplified)
        if numeric_stats:
            outlier_cols = []
            for col, stats in numeric_stats.items():
                mean_val = stats.get('mean', 0)
                std_val = stats.get('std', 0)
                min_val = stats.get('min', 0)
                max_val = stats.get('max', 0)
                
                # Simple outlier detection
                if abs(max_val - mean_val) > 3 * std_val or abs(min_val - mean_val) > 3 * std_val:
                    outlier_cols.append(col)
            
            if outlier_cols:
                insights.append(f"⚠ <b>Potential Outliers</b>: Detected in columns: {', '.join(outlier_cols[:3])}")
            else:
                insights.append("✓ <b>No Obvious Outliers</b>: Data appears normally distributed")
        
        for insight in insights:
            elements.append(Paragraph(insight, self.styles['CustomBody']))
            elements.append(Spacer(1, 4))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_frequencies_section(self, pdf_data):
        """Build categorical frequencies section"""
        elements = []
        
        elements.append(Paragraph(get_text('CATEGORICAL_FREQUENCIES', self.language), self.styles['CustomSubtitle']))
        
        categorical_freqs = pdf_data.get('categorical_freqs', {})
        if categorical_freqs:
            for col, freqs in categorical_freqs.items():
                elements.append(Paragraph(f"<b>{col}:</b>", self.styles['CustomBody']))
                
                table_data = [[get_text('VALUE', self.language), get_text('FREQUENCY', self.language)]]
                for value, freq in list(freqs.items())[:5]:
                    table_data.append([str(value), str(freq)])
                
                if len(freqs) > 5:
                    table_data.append(['...', f'and {len(freqs) - 5} more values'])
                
                table = Table(table_data, colWidths=[3*inch, 1.5*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_custom_chart_section(self, pdf_data):
        """Build custom chart section"""
        elements = []
        
        elements.append(Paragraph(get_text('CHART_SECTION', self.language), self.styles['CustomSubtitle']))
        
        custom_chart = pdf_data.get('custom_chart', {})
        chart_type = custom_chart.get('type')
        
        if chart_type == 'bars':
            elements.extend(self._render_bar_chart(custom_chart))
        elif chart_type == 'scatter':
            elements.extend(self._render_scatter_chart(custom_chart))
        elif chart_type == 'line':
            elements.extend(self._render_line_chart(custom_chart))
        else:
            elements.append(Paragraph(get_text('UNSUPPORTED_CHART_TYPE', self.language), self.styles['CustomBody']))
            logger.warning(f"Unsupported chart type: {chart_type}")
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _render_bar_chart(self, chart_data):
        """Render bar chart"""
        elements = []
        
        try:
            categories = chart_data.get('categories', [])
            values = chart_data.get('values', [])
            title = chart_data.get('title', 'Bar Chart')
            
            numeric_values = []
            for value in values:
                try:
                    numeric_values.append(float(value))
                except (ValueError, TypeError):
                    pass
            
            if categories and numeric_values and len(categories) == len(numeric_values):
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(range(len(categories)), numeric_values, color='#3498db', alpha=0.8)
                ax.set_title(title, fontsize=14, fontweight='bold')
                ax.set_xlabel('Categories', fontsize=12)
                ax.set_ylabel('Values', fontsize=12)
                
                ax.set_xticks(range(len(categories)))
                ax.set_xticklabels(categories, rotation=45, ha='right')
                
                for bar, value in zip(bars, numeric_values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + max(numeric_values)*0.01,
                            f'{value:.0f}', ha='center', va='bottom', fontsize=10)
                
                ax.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                
                image = self._render_chart_to_image(fig, width=7*inch, height=4*inch)
                if image:
                    elements.append(image)
                    elements.append(Spacer(1, 12))
                
                plt.close(fig)
            else:
                elements.append(Paragraph("Incompatible data for bar chart", self.styles['CustomBody']))
                
        except Exception as e:
            logger.error(f"Bar chart rendering failed: {e}")
            elements.append(Paragraph("Error generating bar chart", self.styles['CustomBody']))
        
        return elements
    
    def _render_scatter_chart(self, chart_data):
        """Render scatter chart"""
        elements = []
        
        try:
            x_data = chart_data.get('x_data', [])
            y_data = chart_data.get('y_data', [])
            x_label = chart_data.get('x_label', 'X')
            y_label = chart_data.get('y_label', 'Y')
            title = chart_data.get('title', 'Scatter Plot')
            
            x_numeric = []
            y_numeric = []
            
            for value in x_data:
                try:
                    x_numeric.append(float(value))
                except (ValueError, TypeError):
                    pass
            
            for value in y_data:
                try:
                    y_numeric.append(float(value))
                except (ValueError, TypeError):
                    pass
            
            if x_numeric and y_numeric and len(x_numeric) == len(y_numeric):
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(x_numeric, y_numeric, alpha=0.6, color='#2ecc71', s=30)
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_title(title)
                ax.grid(True, alpha=0.3)
                
                image = self._render_chart_to_image(fig, width=6*inch, height=4.5*inch)
                if image:
                    elements.append(image)
                    elements.append(Spacer(1, 12))
                
                plt.close(fig)
            else:
                elements.append(Paragraph("Incompatible data for scatter plot", self.styles['CustomBody']))
                
        except Exception as e:
            logger.error(f"Scatter chart rendering failed: {e}")
            elements.append(Paragraph("Error generating scatter plot", self.styles['CustomBody']))
        
        return elements
    
    def _render_line_chart(self, chart_data):
        """Render line chart"""
        elements = []
        
        try:
            x_data = chart_data.get('x_data', [])
            y_data = chart_data.get('y_data', [])
            x_label = chart_data.get('x_label', 'X')
            y_label = chart_data.get('y_label', 'Y')
            title = chart_data.get('title', 'Line Chart')
            
            x_numeric = []
            y_numeric = []
            
            for value in x_data:
                try:
                    x_numeric.append(float(value))
                except (ValueError, TypeError):
                    pass
            
            for value in y_data:
                try:
                    y_numeric.append(float(value))
                except (ValueError, TypeError):
                    pass
            
            if x_numeric and y_numeric and len(x_numeric) == len(y_numeric):
                sorted_data = sorted(zip(x_numeric, y_numeric), key=lambda x: x[0])
                x_sorted, y_sorted = zip(*sorted_data)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                ax.plot(x_sorted, y_sorted, 
                       marker='o', 
                       linewidth=3, 
                       markersize=8, 
                       color='#3498db', 
                       alpha=0.9,
                       markerfacecolor='#3498db',
                       markeredgecolor='white',
                       markeredgewidth=2)
                
                ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
                ax.set_ylabel(y_label, fontsize=12, fontweight='bold')
                ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
                
                ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
                
                x_min, x_max = min(x_sorted), max(x_sorted)
                y_min, y_max = min(y_sorted), max(y_sorted)
                x_padding = (x_max - x_min) * 0.1
                y_padding = (y_max - y_min) * 0.1
                
                ax.set_xlim(x_min - x_padding, x_max + x_padding)
                ax.set_ylim(y_min - y_padding, y_max + y_padding)
                
                for x, y in zip(x_sorted, y_sorted):
                    ax.annotate(f'{y:.0f}', 
                              (x, y), 
                              textcoords="offset points", 
                              xytext=(0,15), 
                              ha='center', 
                              va='bottom',
                              fontsize=9,
                              fontweight='bold',
                              color='#2c3e50',
                              bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8, edgecolor='#3498db'))
                
                plt.tight_layout()
                
                image = self._render_chart_to_image(fig, width=7*inch, height=4.5*inch)
                if image:
                    elements.append(image)
                    elements.append(Spacer(1, 12))
                
                plt.close(fig)
            else:
                elements.append(Paragraph("Incompatible data for line chart", self.styles['CustomBody']))
                
        except Exception as e:
            logger.error(f"Line chart rendering failed: {e}")
            elements.append(Paragraph("Error generating line chart", self.styles['CustomBody']))
        
        return elements
    
    def _build_cleaning_notes_section(self, pdf_data):
        """Build cleaning notes section"""
        elements = []
        
        elements.append(Paragraph(get_text('CLEANING_NOTES', self.language), self.styles['CustomSubtitle']))
        
        cleaning_notes = pdf_data.get('cleaning_notes', {})
        if cleaning_notes:
            elements.append(Paragraph(f"Applied strategy: <b>{cleaning_notes.get('strategy', 'N/A')}</b>", self.styles['CustomBody']))
            elements.append(Paragraph(f"Modified rows: <b>{cleaning_notes.get('modified_rows', 0)}</b>", self.styles['CustomBody']))
            elements.append(Paragraph(f"Filled values: <b>{cleaning_notes.get('filled_values', 0)}</b>", self.styles['CustomBody']))
            elements.append(Paragraph(f"Cleaning date: <b>{cleaning_notes.get('date', 'N/A')}</b>", self.styles['CustomBody']))
        else:
            elements.append(Paragraph("No cleaning strategy was applied.", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        return elements
    
    def _build_recommendations_section(self, pdf_data):
        """Build recommendations section"""
        elements = []
        
        elements.append(Paragraph(get_text('OBSERVATIONS_AND_RECOMMENDATIONS', self.language), self.styles['CustomSubtitle']))
        
        recommendations = []
        
        missing_total = pdf_data.get('missing_total', 0)
        total_rows = pdf_data.get('summary', {}).get('rows', 0)
        total_cols = pdf_data.get('summary', {}).get('columns', 1)
        numeric_stats = pdf_data.get('numeric_stats', {})
        categorical_freqs = pdf_data.get('categorical_freqs', {})
        
        # Data quality recommendations
        if missing_total > 0:
            missing_percentage = (missing_total / (total_rows * total_cols)) * 100
            if missing_percentage > 20:
                recommendations.append(get_text('CRITICAL_HIGH_MISSING', self.language))
            elif missing_percentage > 5:
                recommendations.append(get_text('WARNING_MODERATE_MISSING', self.language))
            else:
                recommendations.append(get_text('GOOD_LOW_MISSING', self.language))
        
        # Column-specific recommendations
        missing_by_column = pdf_data.get('missing_by_column', {})
        for col, count in missing_by_column.items():
            if count > 0:
                col_percentage = (count / total_rows) * 100 if total_rows > 0 else 0
                if col_percentage > 50:
                    recommendations.append(get_text('CRITICAL_COLUMN_MISSING', self.language, col=col, percentage=col_percentage))
                elif col_percentage > 30:
                    recommendations.append(get_text('WARNING_COLUMN_MISSING', self.language, col=col, percentage=col_percentage))
                elif col_percentage > 10:
                    recommendations.append(get_text('INFO_COLUMN_MISSING', self.language, col=col, percentage=col_percentage))
        
        # Statistical recommendations
        for col, stats in numeric_stats.items():
            mean_val = stats.get('mean', 0)
            std_val = stats.get('std', 0)
            min_val = stats.get('min', 0)
            max_val = stats.get('max', 0)
            
            # Check for high dispersion
            if std_val > mean_val * 0.5 and mean_val != 0:
                recommendations.append(get_text('RECOMMENDATION_HIGH_VARIABILITY', self.language, column=col))
            
            # Check for potential outliers
            if abs(max_val - mean_val) > 3 * std_val or abs(min_val - mean_val) > 3 * std_val:
                recommendations.append(get_text('RECOMMENDATION_OUTLIERS', self.language, column=col))
            
            # Check for skewed data
            if abs(max_val - mean_val) > 2 * abs(min_val - mean_val) or abs(min_val - mean_val) > 2 * abs(max_val - mean_val):
                recommendations.append(get_text('RECOMMENDATION_SKEWNESS', self.language, column=col))
        
        # Categorical data recommendations
        for col, freqs in categorical_freqs.items():
            unique_count = len(freqs)
            total_count = sum(freqs.values())
            
            if unique_count > total_count * 0.5:
                recommendations.append(get_text('WARNING_HIGH_CARDINALITY', self.language, col=col, n=unique_count))
            
            # Check for imbalanced categories
            max_freq = max(freqs.values())
            min_freq = min(freqs.values())
            if max_freq > min_freq * 10:
                recommendations.append(get_text('RECOMMENDATION_IMBALANCED', self.language, column=col))
        
        # Dataset size recommendations
        if total_rows < 50:
            recommendations.append(get_text('RECOMMENDATION_SAMPLE_SIZE', self.language))
        elif total_rows < 100:
            recommendations.append(get_text('RECOMMENDATION_MODERATE_SAMPLE', self.language))
        else:
            recommendations.append(get_text('RECOMMENDATION_GOOD_SAMPLE', self.language))
        
        # Analysis recommendations
        if numeric_stats and categorical_freqs:
            recommendations.append(get_text('RECOMMENDATION_MIXED_ANALYSIS', self.language))
        elif numeric_stats:
            recommendations.append(get_text('RECOMMENDATION_NUMERIC_ANALYSIS', self.language))
        elif categorical_freqs:
            recommendations.append(get_text('RECOMMENDATION_CATEGORICAL_ANALYSIS', self.language))
        
        if not recommendations:
            recommendations.append(get_text('RECOMMENDATION_EXCELLENT_QUALITY', self.language))
        
        # Group recommendations by priority
        critical_recs = [r for r in recommendations if "🔴" in r]
        warning_recs = [r for r in recommendations if "🟡" in r]
        info_recs = [r for r in recommendations if "🟢" in r]
        
        if critical_recs:
            elements.append(Paragraph(get_text('CRITICAL_ISSUES', self.language), self.styles['CustomBody']))
            for rec in critical_recs:
                elements.append(Paragraph(f"• {rec.replace('🔴', '')}", self.styles['CustomBody']))
                elements.append(Spacer(1, 4))
            elements.append(Spacer(1, 8))
        
        if warning_recs:
            elements.append(Paragraph(get_text('WARNINGS', self.language), self.styles['CustomBody']))
            for rec in warning_recs:
                elements.append(Paragraph(f"• {rec.replace('🟡', '')}", self.styles['CustomBody']))
                elements.append(Spacer(1, 4))
            elements.append(Spacer(1, 8))
        
        if info_recs:
            elements.append(Paragraph(get_text('INFORMATION', self.language), self.styles['CustomBody']))
            for rec in info_recs:
                elements.append(Paragraph(f"• {rec.replace('🟢', '')}", self.styles['CustomBody']))
                elements.append(Spacer(1, 4))
        
        elements.append(Spacer(1, 20))
        return elements 