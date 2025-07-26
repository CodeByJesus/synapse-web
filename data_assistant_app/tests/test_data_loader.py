import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from django.test import TestCase
from ..data_loader import DataLoader

class TestDataLoader(TestCase):
    """Test cases for DataLoader functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = {
            'Name': ['John', 'Jane', 'Bob', None, 'Alice'],
            'Age': [25, 30, None, 35, 28],
            'Income': [50000, 60000, 45000, None, 55000],
            'City': ['NYC', 'LA', 'Chicago', 'Boston', None]
        }
        self.df = pd.DataFrame(self.test_data)
    
    def test_analyze_dataset_basic(self):
        """Test basic dataset analysis"""
        analysis = DataLoader.analyze_dataset(self.df)
        
        # Check summary
        self.assertEqual(analysis['summary']['rows'], 5)
        self.assertEqual(analysis['summary']['columns'], 4)
        
        # Check missing values
        self.assertEqual(analysis['missing_values']['total'], 3)
        self.assertIn('Age', analysis['missing_values']['by_column'])
        self.assertIn('Income', analysis['missing_values']['by_column'])
        
        # Check numeric stats
        self.assertIn('Age', analysis['numeric_stats'])
        self.assertIn('Income', analysis['numeric_stats'])
        
        # Check categorical freqs
        self.assertIn('Name', analysis['categorical_freqs'])
        self.assertIn('City', analysis['categorical_freqs'])
    
    def test_clean_dataset_remove_missing(self):
        """Test remove missing values strategy"""
        cleaned_df = DataLoader.clean_dataset(self.df.copy(), 'remove_missing')
        
        # Should have fewer rows after removing NaN
        self.assertLess(cleaned_df.shape[0], self.df.shape[0])
        self.assertEqual(cleaned_df.isnull().sum().sum(), 0)
    
    def test_clean_dataset_fill_mean(self):
        """Test fill mean strategy"""
        cleaned_df = DataLoader.clean_dataset(self.df.copy(), 'fill_mean')
        
        # Should have same number of rows
        self.assertEqual(cleaned_df.shape[0], self.df.shape[0])
        
        # Numeric columns should have no NaN
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.assertEqual(cleaned_df[col].isnull().sum(), 0)
    
    def test_clean_dataset_fill_zero(self):
        """Test fill zero strategy"""
        cleaned_df = DataLoader.clean_dataset(self.df.copy(), 'fill_zero')
        
        # Numeric columns should have no NaN
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.assertEqual(cleaned_df[col].isnull().sum(), 0)
            # Check that NaN were replaced with 0
            original_nan_count = self.df[col].isnull().sum()
            if original_nan_count > 0:
                self.assertEqual((cleaned_df[col] == 0).sum(), original_nan_count)
    
    def test_load_dataset_csv(self):
        """Test CSV file loading"""
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            self.df.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            loaded_df = DataLoader.load_dataset(temp_file)
            self.assertTrue(loaded_df.equals(self.df))
        finally:
            os.unlink(temp_file)
    
    def test_load_dataset_unsupported_format(self):
        """Test handling of unsupported file format"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"test data")
            temp_file = f.name
        
        try:
            with self.assertRaises(ValueError):
                DataLoader.load_dataset(temp_file)
        finally:
            os.unlink(temp_file)
    
    def test_analyze_dataset_empty(self):
        """Test analysis of empty dataset"""
        empty_df = pd.DataFrame()
        analysis = DataLoader.analyze_dataset(empty_df)
        
        self.assertEqual(analysis['summary']['rows'], 0)
        self.assertEqual(analysis['summary']['columns'], 0)
        self.assertEqual(analysis['missing_values']['total'], 0)
    
    def test_clean_dataset_invalid_strategy(self):
        """Test handling of invalid cleaning strategy"""
        with self.assertRaises(Exception):
            DataLoader.clean_dataset(self.df.copy(), 'invalid_strategy')

if __name__ == '__main__':
    pytest.main([__file__]) 