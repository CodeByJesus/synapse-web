from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import os
import json
import logging
from django.conf import settings
from datetime import datetime
from .pdf_generator import PDFGenerator
from .data_loader import DataLoader
from .utils_pdf import PDFDataPreparer
from .error_handler import ErrorHandler
from .translations import get_text
import glob

logger = logging.getLogger(__name__)

# File extensions supported by the application
SUPPORTED_EXTENSIONS = ["*.csv", "*.xlsx", "*.xls", "*.pdf"]

# Strategy mapping for data cleaning
CLEANING_STRATEGIES = {
    'eliminar_nan': 'remove_missing',
    'imputar_promedio': 'fill_mean',
    'imputar_mediana': 'fill_median',
    'imputar_moda': 'fill_mode',
    'imputar_cero': 'fill_zero'
}

def get_all_files():
    """Get all supported files from media directory"""
    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        all_files.extend(glob.glob(os.path.join(settings.MEDIA_ROOT, ext)))
    return all_files

def cleanup_old_files():
    """Auto-cleanup to prevent file accumulation"""
    try:
        all_files = get_all_files()
        all_files.sort(key=os.path.getmtime)
        
        files_to_remove = all_files[:-3] if len(all_files) > 3 else []
        
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                ErrorHandler.log_file_operation("cleanup", file_path, success=True)
            except OSError as e:
                ErrorHandler.log_file_operation("cleanup", file_path, success=False)
                logger.warning(f"Failed to remove {file_path}: {e}")
                
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def purge_all_files():
    """Remove all data and report files"""
    try:
        all_files = get_all_files()
        removed_files = []
        
        for file_path in all_files:
            try:
                os.remove(file_path)
                removed_files.append(os.path.basename(file_path))
                ErrorHandler.log_file_operation("purge", file_path, success=True)
            except OSError as e:
                ErrorHandler.log_file_operation("purge", file_path, success=False)
                logger.warning(f"Failed to remove {file_path}: {e}")
        
        return removed_files
                
    except Exception as e:
        logger.error(f"Purge error: {e}")
        return []

def append_timestamp_to_filename(original_name):
    """Add timestamp to filename to avoid conflicts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(original_name)[0]
    extension = os.path.splitext(original_name)[1]
    return f"{base_name}_{timestamp}{extension}"

def render_home_with_analysis(request, dataset, filename, uploaded_file_url=None, error=None):
    """Render home template with dataset analysis"""
    # Get current language from session, default to English
    language = request.session.get('language', 'en')
    
    context = {
        'uploaded_file_url': uploaded_file_url,
        'filename': filename,
        'error': error,
        'summary': None,
        'missing_total': 0,
        'missing_by_column': {},
        'rows_with_missing': [],
        'numeric_stats': {},
        'categorical_freqs': {},
        'language': language,
        'translations': {
            'LANGUAGE_SELECTOR': get_text('LANGUAGE_SELECTOR', language),
            'SPANISH': get_text('SPANISH', language),
            'ENGLISH': get_text('ENGLISH', language),
            'DATA_VISUALIZATION': get_text('DATA_VISUALIZATION', language),
            'CHART_TYPE': get_text('CHART_TYPE', language),
            'X_AXIS': get_text('X_AXIS', language),
            'Y_AXIS': get_text('Y_AXIS', language),
            'GENERATE_CHART': get_text('GENERATE_CHART', language),
            'EXPORT_REPORT': get_text('EXPORT_REPORT', language),
            'DOWNLOAD_PDF': get_text('DOWNLOAD_PDF', language),
            'UPLOAD_FILE': get_text('UPLOAD_FILE', language),
            'ANALYZE_DATA': get_text('ANALYZE_DATA', language),
            'UPLOAD_YOUR_DATA_FILE': get_text('UPLOAD_YOUR_DATA_FILE', language),
            'DRAG_AND_DROP': get_text('DRAG_AND_DROP', language),
            'CLEAN_ALL_FILES': get_text('CLEAN_ALL_FILES', language),
            'FILE_UPLOADED': get_text('FILE_UPLOADED', language),
            'DATASET_OVERVIEW': get_text('DATASET_OVERVIEW', language),
            'ROWS': get_text('ROWS', language),
            'COLUMNS': get_text('COLUMNS', language),
            'FIRST_ROWS': get_text('FIRST_ROWS', language),
            'MISSING_VALUES_ANALYSIS': get_text('MISSING_VALUES_ANALYSIS', language),
            'TOTAL_MISSING': get_text('TOTAL_MISSING', language),
            'MISSING_BY_COLUMN': get_text('MISSING_BY_COLUMN', language),
            'EXAMPLES_INCOMPLETE': get_text('EXAMPLES_INCOMPLETE', language),
            'CLEANING_OPTIONS': get_text('CLEANING_OPTIONS', language),
            'REMOVE_MISSING': get_text('REMOVE_MISSING', language),
            'FILL_WITH_MEAN': get_text('FILL_WITH_MEAN', language),
            'FILL_WITH_MEDIAN': get_text('FILL_WITH_MEDIAN', language),
            'FILL_WITH_MODE': get_text('FILL_WITH_MODE', language),
            'FILL_WITH_ZERO': get_text('FILL_WITH_ZERO', language),
            'REVERT_CHANGES': get_text('REVERT_CHANGES', language),
            'DESCRIPTIVE_STATISTICS_TITLE': get_text('DESCRIPTIVE_STATISTICS_TITLE', language),
            'CATEGORICAL_FREQUENCIES_TITLE': get_text('CATEGORICAL_FREQUENCIES_TITLE', language),
            'GENERATE_COMPREHENSIVE_REPORT': get_text('GENERATE_COMPREHENSIVE_REPORT', language),
            'CONNECT': get_text('CONNECT', language),
            'GITHUB': get_text('GITHUB', language),
            'DEVELOPER_SYNAPSE_CREATOR': get_text('DEVELOPER_SYNAPSE_CREATOR', language),
            'LIKE_SYNAPSE_CHECKOUT': get_text('LIKE_SYNAPSE_CHECKOUT', language),
            'APP_TITLE': get_text('APP_TITLE', language),
            'PROFESSIONAL_ASSISTANT': get_text('PROFESSIONAL_ASSISTANT', language),
            'APP_DESCRIPTION': get_text('APP_DESCRIPTION', language),
        }
    }
    
    if dataset is None:
        return render(request, 'home.html', context)
    
    analysis = DataLoader.analyze_dataset(dataset)
    
    # Update context with analysis data
    context.update({
        'uploaded_file_url': uploaded_file_url,
        'filename': filename,
        'summary': {
            'first_rows': dataset.head().to_html(classes='table table-striped', index=False, table_id='main-table'),
            'last_rows': dataset.tail().to_html(classes='table table-striped', index=False),
            'rows': dataset.shape[0],
            'columns': dataset.shape[1],
            'data_types': dataset.dtypes.astype(str).to_dict(),
            'column_names': list(dataset.columns)
        },
        'error': error,
        'missing_total': analysis['missing_values']['total'],
        'missing_by_column': analysis['missing_values']['by_column'],
        'rows_with_missing': analysis['rows_with_missing'],
        'numeric_stats': analysis['numeric_stats'],
        'categorical_freqs': analysis['categorical_freqs'],
    })
    
    return render(request, 'home.html', context)

def handle_file_upload(request):
    """Handle new file upload"""
    try:
        datafile = request.FILES['datafile']
        cleanup_old_files()
        
        new_filename = append_timestamp_to_filename(datafile.name)
        fs = FileSystemStorage()
        filename = fs.save(new_filename, datafile)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        dataset = DataLoader.load_dataset(file_path)
        ErrorHandler.log_data_operation("upload", filename, success=True, user_info="file_upload")
        
        return render_home_with_analysis(request, dataset, filename, fs.url(filename))
        
    except Exception as e:
        error_msg = ErrorHandler.handle_error(request, e, context="file_upload")
        ErrorHandler.log_data_operation("upload", datafile.name if 'datafile' in locals() else 'unknown', success=False)
        return render_home_with_analysis(request, None, filename, error=error_msg)

def handle_data_cleaning(request):
    """Handle data cleaning operations"""
    try:
        filename = request.POST.get('filename')
        strategy = request.POST.get('action')
        
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        dataset = DataLoader.load_dataset(file_path)
        
        if strategy == 'revertir_cambios':
            # Revert to original data
            dataset = DataLoader.load_dataset(file_path)
            ErrorHandler.log_data_operation("revert", filename, success=True)
        else:
            # Apply cleaning strategy using mapping
            clean_strategy = CLEANING_STRATEGIES.get(strategy, 'remove_missing')
            dataset = DataLoader.clean_dataset(dataset, clean_strategy)
            ErrorHandler.log_data_operation(f"clean_{clean_strategy}", filename, success=True)
        
        return render_home_with_analysis(request, dataset, filename)
        
    except Exception as e:
        error_msg = ErrorHandler.handle_error(request, e, context="data_cleaning")
        ErrorHandler.log_data_operation("cleaning", filename, success=False)
        return render_home_with_analysis(request, None, filename, error=error_msg)

def handle_pdf_export(request):
    """Handle PDF export request"""
    try:
        filename = request.POST.get('filename')
        if not filename:
            messages.error(request, 'No file selected for export')
            return redirect('home')
        
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        dataset = DataLoader.load_dataset(file_path)
        analysis = DataLoader.analyze_dataset(dataset)
        analysis['filename'] = filename
        
        chart_config = request.session.get('current_chart', {})
        logger.info(f"Retrieved chart config from session: {chart_config}")
        
        # Get current language for PDF
        language = request.session.get('language', 'en')
        pdf_data = PDFDataPreparer.prepare_pdf_data(dataset, analysis, chart_config)
        
        # Generate PDF with language
        pdf_generator = PDFGenerator(language=language)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"synapse_report_{timestamp}.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
        
        pdf_generator.generate_pdf(pdf_data, pdf_path)
        
        # Download PDF
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        
        # Clean up temporary file
        os.remove(pdf_path)
        
        ErrorHandler.log_data_operation("pdf_export", filename, success=True)
        return response
        
    except Exception as e:
        error_msg = ErrorHandler.handle_error(request, e, context="pdf_export")
        ErrorHandler.log_data_operation("pdf_export", filename, success=False)
        messages.error(request, f'PDF generation failed: {str(e)}')
        return redirect('home')

def handle_chart_save(request):
    """Handle chart configuration save"""
    try:
        chart_data = json.loads(request.POST.get('chart_data', '{}'))
        logger.info(f"Saving chart configuration: {chart_data}")
        request.session['current_chart'] = chart_data
        request.session.modified = True  # Ensure session is saved
        ErrorHandler.log_data_operation("chart_save", "session", success=True)
        logger.info("Chart configuration saved successfully")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        error_msg = ErrorHandler.handle_error(request, e, context="chart_save")
        ErrorHandler.log_data_operation("chart_save", "session", success=False)
        logger.error(f"Failed to save chart configuration: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

def home(request):
    """Main view handler"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'cleanup_files':
            removed_files = purge_all_files()
            if removed_files:
                message = f'Files cleaned: {len(removed_files)} items removed'
            else:
                message = 'No files to clean'
            messages.success(request, message)
            return redirect('home')
        
        elif action == 'save_chart':
            return handle_chart_save(request)
        
        elif action == 'export_pdf':
            return handle_pdf_export(request)
        
        elif action == 'change_language':
            return handle_language_change(request)
        
        elif action in CLEANING_STRATEGIES.keys() or action == 'revertir_cambios':
            return handle_data_cleaning(request)
        
        elif request.FILES.get('datafile'):
            return handle_file_upload(request)
    
    # Get current language from session, default to English
    language = request.session.get('language', 'en')
    
    return render(request, 'home.html', {
        'language': language,
        'translations': {
            'LANGUAGE_SELECTOR': get_text('LANGUAGE_SELECTOR', language),
            'SPANISH': get_text('SPANISH', language),
            'ENGLISH': get_text('ENGLISH', language),
            'DATA_VISUALIZATION': get_text('DATA_VISUALIZATION', language),
            'CHART_TYPE': get_text('CHART_TYPE', language),
            'X_AXIS': get_text('X_AXIS', language),
            'Y_AXIS': get_text('Y_AXIS', language),
            'GENERATE_CHART': get_text('GENERATE_CHART', language),
            'EXPORT_REPORT': get_text('EXPORT_REPORT', language),
            'DOWNLOAD_PDF': get_text('DOWNLOAD_PDF', language),
            'UPLOAD_FILE': get_text('UPLOAD_FILE', language),
            'ANALYZE_DATA': get_text('ANALYZE_DATA', language),
            'UPLOAD_YOUR_DATA_FILE': get_text('UPLOAD_YOUR_DATA_FILE', language),
            'DRAG_AND_DROP': get_text('DRAG_AND_DROP', language),
            'CLEAN_ALL_FILES': get_text('CLEAN_ALL_FILES', language),
            'FILE_UPLOADED': get_text('FILE_UPLOADED', language),
            'DATASET_OVERVIEW': get_text('DATASET_OVERVIEW', language),
            'ROWS': get_text('ROWS', language),
            'COLUMNS': get_text('COLUMNS', language),
            'FIRST_ROWS': get_text('FIRST_ROWS', language),
            'MISSING_VALUES_ANALYSIS': get_text('MISSING_VALUES_ANALYSIS', language),
            'TOTAL_MISSING': get_text('TOTAL_MISSING', language),
            'MISSING_BY_COLUMN': get_text('MISSING_BY_COLUMN', language),
            'EXAMPLES_INCOMPLETE': get_text('EXAMPLES_INCOMPLETE', language),
            'CLEANING_OPTIONS': get_text('CLEANING_OPTIONS', language),
            'REMOVE_MISSING': get_text('REMOVE_MISSING', language),
            'FILL_WITH_MEAN': get_text('FILL_WITH_MEAN', language),
            'FILL_WITH_MEDIAN': get_text('FILL_WITH_MEDIAN', language),
            'FILL_WITH_MODE': get_text('FILL_WITH_MODE', language),
            'FILL_WITH_ZERO': get_text('FILL_WITH_ZERO', language),
            'REVERT_CHANGES': get_text('REVERT_CHANGES', language),
            'DESCRIPTIVE_STATISTICS_TITLE': get_text('DESCRIPTIVE_STATISTICS_TITLE', language),
            'CATEGORICAL_FREQUENCIES_TITLE': get_text('CATEGORICAL_FREQUENCIES_TITLE', language),
            'GENERATE_COMPREHENSIVE_REPORT': get_text('GENERATE_COMPREHENSIVE_REPORT', language),
            'CONNECT': get_text('CONNECT', language),
            'GITHUB': get_text('GITHUB', language),
            'DEVELOPER_SYNAPSE_CREATOR': get_text('DEVELOPER_SYNAPSE_CREATOR', language),
            'LIKE_SYNAPSE_CHECKOUT': get_text('LIKE_SYNAPSE_CHECKOUT', language),
            'APP_TITLE': get_text('APP_TITLE', language),
            'PROFESSIONAL_ASSISTANT': get_text('PROFESSIONAL_ASSISTANT', language),
            'APP_DESCRIPTION': get_text('APP_DESCRIPTION', language),
        }
    })

def handle_language_change(request):
    """Handle language change request"""
    language = request.POST.get('language', 'en')
    if language in ['en', 'es']:
        request.session['language'] = language
        request.session.modified = True
        logger.info(f"Language changed to: {language}")
    
    return JsonResponse({'success': True, 'language': language})
    
