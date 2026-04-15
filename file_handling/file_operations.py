"""
File Handling - Reading and Writing Files
"""

import os
import json
import csv

def read_file(filename):
    """Read a text file and return its content"""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{filename}' not found."

def write_file(filename, content):
    """Write content to a file"""
    with open(filename, 'w') as file:
        file.write(content)
    return f"Content written to '{filename}'"

def append_file(filename, content):
    """Append content to an existing file"""
    with open(filename, 'a') as file:
        file.write(content)
    return f"Content appended to '{filename}'"

def count_lines(filename):
    """Count the number of lines in a file"""
    try:
        with open(filename, 'r') as file:
            return len(file.readlines())
    except FileNotFoundError:
        return 0

def read_json_file(filename):
    """Read a JSON file and return its content as a dictionary"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def write_json_file(filename, data):
    """Write data to a JSON file"""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    return f"Data written to '{filename}'"

def read_csv_file(filename):
    """Read a CSV file and return its content as a list of dictionaries"""
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return None

def write_csv_file(filename, data, fieldnames):
    """Write data to a CSV file"""
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    return f"Data written to '{filename}'"

def create_sample_files():
    """Create sample files for testing"""
    # Create a sample text file
    write_file('sample.txt', 'Hello, World!\nThis is a sample file.\nPython file handling is fun!')
    
    # Create a sample JSON file
    sample_data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York',
        'hobbies': ['reading', 'coding', 'hiking']
    }
    write_json_file('sample.json', sample_data)
    
    # Create a sample CSV file
    csv_data = [
        {'name': 'Alice', 'age': 25, 'city': 'Boston'},
        {'name': 'Bob', 'age': 30, 'city': 'Chicago'},
        {'name': 'Charlie', 'age': 35, 'city': 'Denver'}
    ]
    write_csv_file('sample.csv', csv_data, ['name', 'age', 'city'])

def main():
    # Create sample files
    create_sample_files()
    print("Sample files created.\n")
    
    # Test file reading
    print("Reading sample.txt:")
    print(read_file('sample.txt'))
    print(f"Number of lines: {count_lines('sample.txt')}\n")
    
    # Test JSON operations
    print("Reading sample.json:")
    json_data = read_json_file('sample.json')
    print(json_data)
    print()
    
    # Test CSV operations
    print("Reading sample.csv:")
    csv_data = read_csv_file('sample.csv')
    for row in csv_data:
        print(row)
    print()
    
    # Test appending to file
    append_file('sample.txt', '\nThis line was appended.')
    print("After appending:")
    print(read_file('sample.txt'))
    
    # Cleanup
    os.remove('sample.txt')
    os.remove('sample.json')
    os.remove('sample.csv')
    print("\nSample files cleaned up.")

if __name__ == "__main__":
    main()