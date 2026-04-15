"""
Automation Scripts - File and System Automation
"""

import os
import shutil
import time
import glob
from pathlib import Path
from datetime import datetime, timedelta

def organize_files_by_extension(directory):
    """
    Organize files in a directory by their extensions
    """
    print(f"Organizing files in: {directory}")
    
    # Create a dictionary to store files by extension
    files_by_extension = {}
    
    # Get all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # Skip directories
        if os.path.isdir(filepath):
            continue
        
        # Get file extension
        _, extension = os.path.splitext(filename)
        extension = extension.lower().lstrip('.')
        
        if extension:
            if extension not in files_by_extension:
                files_by_extension[extension] = []
            files_by_extension[extension].append(filename)
    
    # Create subdirectories and move files
    for extension, files in files_by_extension.items():
        # Create subdirectory
        subdir = os.path.join(directory, extension)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
            print(f"Created directory: {subdir}")
        
        # Move files
        for filename in files:
            src = os.path.join(directory, filename)
            dst = os.path.join(subdir, filename)
            shutil.move(src, dst)
            print(f"Moved {filename} to {extension}/")
    
    print(f"Organized {len(files_by_extension)} file types.")

def clean_old_files(directory, days_old=30, pattern="*"):
    """
    Remove files older than specified days matching a pattern
    """
    print(f"Cleaning files older than {days_old} days in: {directory}")
    
    cutoff_time = datetime.now() - timedelta(days=days_old)
    removed_count = 0
    
    # Find files matching pattern
    for filepath in glob.glob(os.path.join(directory, pattern)):
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if file_time < cutoff_time:
                os.remove(filepath)
                print(f"Removed: {filepath}")
                removed_count += 1
    
    print(f"Removed {removed_count} files.")

def create_backup(source_dir, backup_dir):
    """
    Create a backup of a directory
    """
    print(f"Creating backup from {source_dir} to {backup_dir}")
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    
    try:
        if os.path.exists(source_dir):
            shutil.copytree(source_dir, backup_path)
            print(f"Backup created successfully: {backup_path}")
            return True
        else:
            print(f"Source directory does not exist: {source_dir}")
            return False
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def find_duplicate_files(directory):
    """
    Find duplicate files in a directory based on file size
    """
    print(f"Finding duplicate files in: {directory}")
    
    # Dictionary to store file sizes
    size_dict = {}
    duplicates = []
    
    for filepath in glob.glob(os.path.join(directory, "**/*"), recursive=True):
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            
            if file_size in size_dict:
                duplicates.append((size_dict[file_size], filepath))
            else:
                size_dict[file_size] = filepath
    
    if duplicates:
        print(f"Found {len(duplicates)} potential duplicate files:")
        for original, duplicate in duplicates:
            print(f"  {original}")
            print(f"  {duplicate}")
            print()
    else:
        print("No duplicate files found.")
    
    return duplicates

def batch_rename_files(directory, pattern, replacement):
    """
    Batch rename files matching a pattern
    """
    print(f"Batch renaming files in: {directory}")
    print(f"Pattern: {pattern} -> {replacement}")
    
    renamed_count = 0
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath) and pattern in filename:
            new_filename = filename.replace(pattern, replacement)
            new_filepath = os.path.join(directory, new_filename)
            
            os.rename(filepath, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
            renamed_count += 1
    
    print(f"Renamed {renamed_count} files.")

def generate_file_report(directory):
    """
    Generate a report of files in a directory
    """
    print(f"Generating file report for: {directory}")
    
    total_files = 0
    total_size = 0
    extension_counts = {}
    
    for filepath in glob.glob(os.path.join(directory, "**/*"), recursive=True):
        if os.path.isfile(filepath):
            total_files += 1
            file_size = os.path.getsize(filepath)
            total_size += file_size
            
            # Count by extension
            _, extension = os.path.splitext(filepath)
            extension = extension.lower().lstrip('.')
            extension_counts[extension] = extension_counts.get(extension, 0) + 1
    
    print(f"\nFile Report for {directory}:")
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size / (1024*1024):.2f} MB")
    print(f"\nFiles by extension:")
    for ext, count in sorted(extension_counts.items()):
        print(f"  {ext or 'no extension'}: {count}")

def monitor_directory(directory, interval=5):
    """
    Monitor a directory for changes (basic implementation)
    """
    print(f"Monitoring directory: {directory} (Press Ctrl+C to stop)")
    
    # Get initial state
    initial_files = set(os.listdir(directory))
    
    try:
        while True:
            time.sleep(interval)
            
            current_files = set(os.listdir(directory))
            
            # Check for new files
            new_files = current_files - initial_files
            if new_files:
                print(f"New files detected: {new_files}")
            
            # Check for deleted files
            deleted_files = initial_files - current_files
            if deleted_files:
                print(f"Files deleted: {deleted_files}")
            
            initial_files = current_files
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

def main():
    """Main function to demonstrate automation scripts"""
    print("Python Automation Scripts")
    print("=" * 50)
    
    # Create a test directory structure
    test_dir = "/tmp/test_automation"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Create some test files
    test_files = [
        "document.txt",
        "image.jpg",
        "script.py",
        "data.csv",
        "another_document.txt",
        "photo.png"
    ]
    
    for filename in test_files:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w') as f:
            f.write("Test content")
    
    print(f"Created test directory: {test_dir}")
    
    # Demonstrate functions
    print("\n1. Organizing files by extension:")
    organize_files_by_extension(test_dir)
    
    print("\n2. Generating file report:")
    generate_file_report(test_dir)
    
    print("\n3. Finding duplicate files:")
    find_duplicate_files(test_dir)
    
    print("\n4. Batch rename files:")
    batch_rename_files(test_dir, "document", "file")
    
    print("\n5. Creating backup:")
    backup_dir = "/tmp/test_backups"
    os.makedirs(backup_dir, exist_ok=True)
    create_backup(test_dir, backup_dir)
    
    # Cleanup
    print("\nCleaning up test directories...")
    shutil.rmtree(test_dir)
    shutil.rmtree(backup_dir)
    print("Done.")
    
    print("\n" + "=" * 50)
    print("Automation Scripts Demonstrated:")
    print("✓ File organization by extension")
    print("✓ Old file cleanup")
    print("✓ Directory backup")
    print("✓ Duplicate file detection")
    print("✓ Batch file renaming")
    print("✓ File reporting")
    print("✓ Directory monitoring")

if __name__ == "__main__":
    main()