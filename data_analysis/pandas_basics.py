"""
Data Analysis - Pandas Examples
"""

import pandas as pd
import numpy as np
from typing import List, Dict

def create_sample_dataframe():
    """Create a sample DataFrame for analysis"""
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'City': ['New York', 'Chicago', 'Los Angeles', 'Boston', 'Seattle'],
        'Salary': [75000, 82000, 90000, 68000, 85000],
        'Department': ['Engineering', 'Marketing', 'Engineering', 'HR', 'Sales']
    }
    return pd.DataFrame(data)

def basic_dataframe_operations(df):
    """Demonstrate basic DataFrame operations"""
    print("Basic DataFrame Operations")
    print("=" * 50)
    
    print("\n1. First few rows:")
    print(df.head())
    
    print("\n2. DataFrame info:")
    print(df.info())
    
    print("\n3. Statistical summary:")
    print(df.describe())
    
    print("\n4. Column names:")
    print(df.columns.tolist())
    
    print("\n5. Data types:")
    print(df.dtypes)

def filtering_and_sorting(df):
    """Demonstrate filtering and sorting operations"""
    print("\n\nFiltering and Sorting")
    print("=" * 50)
    
    # Filter by condition
    print("\n1. Employees older than 30:")
    print(df[df['Age'] > 30])
    
    print("\n2. Engineering department employees:")
    print(df[df['Department'] == 'Engineering'])
    
    print("\n3. Salary > 80000:")
    print(df[df['Salary'] > 80000])
    
    # Sort by column
    print("\n4. Sorted by Age (ascending):")
    print(df.sort_values('Age'))
    
    print("\n5. Sorted by Salary (descending):")
    print(df.sort_values('Salary', ascending=False))

def groupby_operations(df):
    """Demonstrate groupby operations"""
    print("\n\nGroupBy Operations")
    print("=" * 50)
    
    # Group by department
    print("\n1. Average salary by department:")
    print(df.groupby('Department')['Salary'].mean())
    
    print("\n2. Count by department:")
    print(df.groupby('Department').size())
    
    print("\n3. Max age by department:")
    print(df.groupby('Department')['Age'].max())
    
    print("\n4. Multiple aggregations:")
    print(df.groupby('Department').agg({
        'Salary': ['mean', 'max', 'min'],
        'Age': ['mean', 'count']
    }))

def data_manipulation(df):
    """Demonstrate data manipulation operations"""
    print("\n\nData Manipulation")
    print("=" * 50)
    
    # Add new column
    df['Experience'] = df['Age'] - 22  # Assuming starting work at 22
    print("\n1. Added Experience column:")
    print(df)
    
    # Apply function to column
    df['Salary_Category'] = df['Salary'].apply(
        lambda x: 'High' if x > 80000 else 'Medium' if x > 70000 else 'Low'
    )
    print("\n2. Added Salary_Category column:")
    print(df)
    
    # Drop column
    df_modified = df.drop('Experience', axis=1)
    print("\n3. Dropped Experience column:")
    print(df_modified)

def handling_missing_data():
    """Demonstrate handling missing data"""
    print("\n\nHandling Missing Data")
    print("=" * 50)
    
    # Create DataFrame with missing values
    data_with_missing = {
        'A': [1, 2, np.nan, 4, 5],
        'B': [np.nan, 2, 3, np.nan, 5],
        'C': [1, 2, 3, 4, 5]
    }
    df_missing = pd.DataFrame(data_with_missing)
    
    print("\n1. DataFrame with missing values:")
    print(df_missing)
    
    print("\n2. Drop rows with missing values:")
    print(df_missing.dropna())
    
    print("\n3. Fill missing values with mean:")
    print(df_missing.fillna(df_missing.mean()))
    
    print("\n4. Fill missing values with specific value:")
    print(df_missing.fillna(0))

def time_series_analysis():
    """Demonstrate basic time series analysis"""
    print("\n\nTime Series Analysis")
    print("=" * 50)
    
    # Create time series data
    dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
    values = np.random.randint(50, 100, size=10)
    
    ts_df = pd.DataFrame({'Date': dates, 'Value': values})
    ts_df.set_index('Date', inplace=True)
    
    print("\n1. Time series data:")
    print(ts_df)
    
    print("\n2. Rolling mean (window=3):")
    print(ts_df.rolling(window=3).mean())
    
    print("\n3. Date filtering:")
    print(ts_df['2024-01-05':'2024-01-08'])

def data_visualization_preparation(df):
    """Prepare data for visualization"""
    print("\n\nData Visualization Preparation")
    print("=" * 50)
    
    print("\n1. Salary distribution:")
    salary_stats = df['Salary'].describe()
    print(salary_stats)
    
    print("\n2. Department distribution:")
    dept_counts = df['Department'].value_counts()
    print(dept_counts)
    
    print("\n3. Age vs Salary correlation:")
    correlation = df['Age'].corr(df['Salary'])
    print(f"Correlation coefficient: {correlation:.2f}")

def main():
    """Main function to run data analysis examples"""
    print("Pandas Data Analysis Examples")
    print("=" * 50)
    
    # Create sample data
    df = create_sample_dataframe()
    
    # Run various analyses
    basic_dataframe_operations(df)
    filtering_and_sorting(df.copy())
    groupby_operations(df.copy())
    data_manipulation(df.copy())
    handling_missing_data()
    time_series_analysis()
    data_visualization_preparation(df)
    
    print("\n" + "=" * 50)
    print("\nKey Pandas Operations Covered:")
    print("✓ DataFrame creation and basic operations")
    print("✓ Filtering and sorting")
    print("✓ GroupBy operations")
    print("✓ Data manipulation and feature engineering")
    print("✓ Handling missing data")
    print("✓ Time series basics")
    print("✓ Statistical analysis")

if __name__ == "__main__":
    main()