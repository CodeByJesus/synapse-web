from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling with logging"""
    
    @staticmethod
    def handle_error(request, error, context=None, user_info=None):
        """Handle errors with proper logging and user messaging"""
        error_context = {
            'error': str(error),
            'user': user_info or getattr(request, 'user', 'anonymous'),
            'context': context or 'unknown'
        }
        
        # Log the error with context
        logger.error(f"Error in {error_context['context']}: {error_context['error']} - User: {error_context['user']}")
        
        # Return user-friendly message
        return f"Operation failed: {str(error)}"
    
    @staticmethod
    def log_file_operation(operation, file_path, success=True, user_info=None):
        """Log file operations with context"""
        status = "successful" if success else "failed"
        logger.info(f"File operation {operation} {status} for {file_path} - User: {user_info or 'unknown'}")
    
    @staticmethod
    def log_data_operation(operation, dataset_info, success=True, user_info=None):
        """Log data operations with context"""
        status = "successful" if success else "failed"
        logger.info(f"Data operation {operation} {status} for {dataset_info} - User: {user_info or 'unknown'}") 