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