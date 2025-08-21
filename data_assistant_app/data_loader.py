import pandas as pd
import numpy as np
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Handles data loading and cleaning operations"""
    
    @staticmethod
    def load_dataset(file_path):
        """Load dataset based on file extension"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            logger.error(f"Failed to load dataset from {file_path}: {e}")
            raise
    
    @staticmethod
    def analyze_dataset(dataset):
        """Generate comprehensive dataset analysis"""
        analysis = {
            'summary': {
                'rows': dataset.shape[0],
                'columns': dataset.shape[1],
                'data_types': dataset.dtypes.astype(str).to_dict()
            },
            'missing_values': {
                'total': int(dataset.isnull().sum().sum()),
                'by_column': dataset.isnull().sum().to_dict()
            },
            'rows_with_missing': [],
            'numeric_stats': {},
            'categorical_freqs': {}
        }
        
        # Find rows with missing values
        for idx, row in dataset.iterrows():
            if row.isnull().any():
                analysis['rows_with_missing'].append({
                    'index': idx,
                    'missing_columns': row[row.isnull()].index.tolist(),
                    'available_data': row.dropna().to_dict()
                })
        
        # Numeric statistics
        for col in dataset.select_dtypes(include=[np.number]).columns:
            analysis['numeric_stats'][col] = {
                'mean': float(dataset[col].mean()),
                'median': float(dataset[col].median()),
                'std': float(dataset[col].std()),
                'min': float(dataset[col].min()),
                'max': float(dataset[col].max()),
                'q1': float(dataset[col].quantile(0.25)),
                'q3': float(dataset[col].quantile(0.75)),
            }
        
        # Categorical frequencies
        for col in dataset.select_dtypes(include=['object', 'category']).columns:
            analysis['categorical_freqs'][col] = dataset[col].value_counts().to_dict()
        
        return analysis
    
    @staticmethod
    def clean_dataset(dataset, strategy):
        """Apply data cleaning strategy"""
        try:
            if strategy == 'remove_missing':
                return dataset.dropna()
            elif strategy == 'fill_mean':
                for col in dataset.select_dtypes(include=[np.number]).columns:
                    dataset[col] = dataset[col].fillna(dataset[col].mean())
            elif strategy == 'fill_median':
                for col in dataset.select_dtypes(include=[np.number]).columns:
                    dataset[col] = dataset[col].fillna(dataset[col].median())
            elif strategy == 'fill_mode':
                for col in dataset.columns:
                    if dataset[col].dtype == 'object':
                        mode_value = dataset[col].mode()[0] if len(dataset[col].mode()) > 0 else 'Unknown'
                        dataset[col] = dataset[col].fillna(mode_value)
                    else:
                        dataset[col] = dataset[col].fillna(dataset[col].median())
            elif strategy == 'fill_zero':
                for col in dataset.select_dtypes(include=[np.number]).columns:
                    dataset[col] = dataset[col].fillna(0)
            
            logger.info(f"Applied cleaning strategy: {strategy}")
            return dataset
            
        except Exception as e:
            logger.error(f"Error applying cleaning strategy {strategy}: {e}")
            raise 
    
    @staticmethod
    def load_large_dataset(file_path, chunk_size=10000):
        """Load large dataset using chunking to avoid memory issues"""
        try:
            logger.info(f"Loading large dataset: {file_path}")
            
            # Determine file type
            if file_path.endswith('.csv'):
                # Count total rows for progress tracking
                total_rows = sum(1 for _ in open(file_path)) - 1  # -1 for header
                logger.info(f"Total rows to process: {total_rows}")
                
                # Process in chunks
                chunks = []
                processed_rows = 0
                
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    processed_rows += len(chunk)
                    progress = (processed_rows / total_rows) * 100 if total_rows > 0 else 0
                    
                    logger.info(f"Processing chunk: {progress:.1f}% complete ({processed_rows}/{total_rows} rows)")
                    
                    # Basic cleaning per chunk
                    chunk_cleaned = chunk.dropna()
                    chunks.append(chunk_cleaned)
                
                # Combine all chunks
                final_dataset = pd.concat(chunks, ignore_index=True)
                logger.info(f"Large dataset loaded successfully: {len(final_dataset)} rows")
                
                return final_dataset
                
            elif file_path.endswith('.xlsx'):
                # For Excel files, load normally but with memory optimization
                return pd.read_excel(file_path, engine='openpyxl')
            else:
                raise ValueError("Unsupported file format for large dataset")
                
        except Exception as e:
            logger.error(f"Failed to load large dataset from {file_path}: {e}")
            raise 