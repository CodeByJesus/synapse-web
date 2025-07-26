#!/usr/bin/env python3
"""
Synapse Data Platform - File Cleanup Utility

Manual file cleanup script for Synapse data files.
Author: jesus.martinez@synapse.es
Date: 26/07/2025
"""

import os
import glob
from datetime import datetime


def display_current_files():
    """Display all CSV and Excel files in the current directory"""
    print("=" * 50)
    print("CURRENT FILES IN DIRECTORY:")
    print("=" * 50)
    
    # Find CSV and Excel files
    csv_files = glob.glob("*.csv")
    excel_files = glob.glob("*.xlsx")
    excel_files.extend(glob.glob("*.xls"))
    
    all_files = csv_files + excel_files
    
    if not all_files:
        print("No CSV or Excel files found.")
        return []
    
    # Display files with information
    for i, filename in enumerate(all_files, 1):
        # Get file information
        stat = os.stat(filename)
        mod_date = datetime.fromtimestamp(stat.st_mtime)
        file_size = stat.st_size
        
        print(f"{i:2d}. {filename}")
        print(f"    Date: {mod_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Size: {file_size} bytes")
        print()
    
    return all_files


def cleanup_files_manual():
    """Allow user to choose which files to delete"""
    files = display_current_files()
    
    if not files:
        return
    
    print("=" * 50)
    print("CLEANUP OPTIONS:")
    print("=" * 50)
    print("1. Delete older files (keep last 3)")
    print("2. Delete specific files")
    print("3. Delete all test files")
    print("4. Exit without changes")
    
    while True:
        try:
            option = input("\nChoose an option (1-4): ").strip()
            
            if option == "1":
                delete_older_files(files, 3)
                break
            elif option == "2":
                delete_specific_files(files)
                break
            elif option == "3":
                delete_test_files(files)
                break
            elif option == "4":
                print("No files were deleted.")
                break
            else:
                print("Invalid option. Please choose 1, 2, 3 or 4.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break


def delete_older_files(files, keep_count=3):
    """Delete older files, keeping only the last N files"""
    if len(files) <= keep_count:
        print(f"Only {len(files)} files found. No cleanup needed.")
        return
    
    # Sort by modification date (oldest first)
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(x))
    files_to_delete = sorted_files[:-keep_count]
    
    print(f"\nWill delete {len(files_to_delete)} older files:")
    for filename in files_to_delete:
        print(f"  - {filename}")
    
    confirmation = input("\nAre you sure? (y/N): ").strip().lower()
    if confirmation == 'y':
        for filename in files_to_delete:
            try:
                os.remove(filename)
                print(f"✓ Deleted: {filename}")
            except Exception as e:
                print(f"✗ Error deleting {filename}: {e}")
        print(f"\nDeleted {len(files_to_delete)} files.")
    else:
        print("Operation cancelled.")


def delete_specific_files(files):
    """Allow user to choose specific files to delete"""
    print("\nChoose files to delete (numbers separated by commas):")
    print("Example: 1,3,5")
    
    try:
        selection = input("Files to delete: ").strip()
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        
        files_to_delete = []
        for i in indices:
            if 0 <= i < len(files):
                files_to_delete.append(files[i])
            else:
                print(f"Index {i+1} is invalid.")
        
        if files_to_delete:
            print(f"\nWill delete {len(files_to_delete)} files:")
            for filename in files_to_delete:
                print(f"  - {filename}")
            
            confirmation = input("\nAre you sure? (y/N): ").strip().lower()
            if confirmation == 'y':
                for filename in files_to_delete:
                    try:
                        os.remove(filename)
                        print(f"✓ Deleted: {filename}")
                    except Exception as e:
                        print(f"✗ Error deleting {filename}: {e}")
                print(f"\nDeleted {len(files_to_delete)} files.")
            else:
                print("Operation cancelled.")
        else:
            print("No valid files selected.")
    except ValueError:
        print("Incorrect format. Use numbers separated by commas.")


def delete_test_files(files):
    """Delete files containing 'test' in the filename"""
    test_files = [f for f in files if 'test' in f.lower()]
    
    if not test_files:
        print("No test files found.")
        return
    
    print(f"\nFound {len(test_files)} test files:")
    for filename in test_files:
        print(f"  - {filename}")
    
    confirmation = input("\nDelete all test files? (y/N): ").strip().lower()
    if confirmation == 'y':
        for filename in test_files:
            try:
                os.remove(filename)
                print(f"✓ Deleted: {filename}")
            except Exception as e:
                print(f"✗ Error deleting {filename}: {e}")
        print(f"\nDeleted {len(test_files)} test files.")
    else:
        print("Operation cancelled.")


def main():
    """Main function of the script"""
    print("SYNAPSE FILE CLEANUP UTILITY")
    print("=" * 50)
    print(f"Current directory: {os.getcwd()}")
    print(f"Date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        cleanup_files_manual()
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("Script completed.")
    print("=" * 50)


if __name__ == "__main__":
    main() 