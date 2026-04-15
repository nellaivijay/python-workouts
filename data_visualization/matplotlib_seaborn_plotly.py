"""
Data Visualization - Matplotlib, Seaborn, and Plotly Examples
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn')
sns.set_palette("husl")


def create_sample_data():
    """Create sample data for visualization"""
    np.random.seed(42)
    
    # Time series data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    values = np.cumsum(np.random.randn(100)) + 100
    time_series_df = pd.DataFrame({'date': dates, 'value': values})
    
    # Categorical data
    categories = ['A', 'B', 'C', 'D', 'E']
    category_data = pd.DataFrame({
        'category': np.random.choice(categories, 200),
        'value': np.random.randint(10, 100, 200)
    })
    
    # Correlation data
    corr_data = pd.DataFrame(np.random.randn(100, 4), columns=['A', 'B', 'C', 'D'])
    
    return time_series_df, category_data, corr_data


def matplotlib_examples(time_series_df, category_data, corr_data):
    """Demonstrate Matplotlib plotting"""
    print("Matplotlib Examples:")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Line plot
    axes[0, 0].plot(time_series_df['date'], time_series_df['value'])
    axes[0, 0].set_title('Time Series Line Plot')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Value')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Bar plot
    category_means = category_data.groupby('category')['value'].mean()
    axes[0, 1].bar(category_means.index, category_means.values)
    axes[0, 1].set_title('Average Value by Category')
    axes[0, 1].set_xlabel('Category')
    axes[0, 1].set_ylabel('Average Value')
    
    # Histogram
    axes[1, 0].hist(category_data['value'], bins=20, edgecolor='black')
    axes[1, 0].set_title('Value Distribution')
    axes[1, 0].set_xlabel('Value')
    axes[1, 0].set_ylabel('Frequency')
    
    # Scatter plot
    axes[1, 1].scatter(corr_data['A'], corr_data['B'], alpha=0.6)
    axes[1, 1].set_title('Scatter Plot: A vs B')
    axes[1, 1].set_xlabel('A')
    axes[1, 1].set_ylabel('B')
    
    plt.tight_layout()
    plt.savefig('/tmp/matplotlib_examples.png', dpi=100)
    print("Saved: /tmp/matplotlib_examples.png")
    plt.close()


def seaborn_examples(category_data, corr_data):
    """Demonstrate Seaborn plotting"""
    print("Seaborn Examples:")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Box plot
    sns.boxplot(data=category_data, x='category', y='value', ax=axes[0, 0])
    axes[0, 0].set_title('Box Plot by Category')
    
    # Violin plot
    sns.violinplot(data=category_data, x='category', y='value', ax=axes[0, 1])
    axes[0, 1].set_title('Violin Plot by Category')
    
    # Heatmap
    correlation_matrix = corr_data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[1, 0])
    axes[1, 0].set_title('Correlation Heatmap')
    
    # Pair plot (subset of data)
    plot_data = corr_data.iloc[:50]
    sns.pairplot(plot_data)
    plt.savefig('/tmp/seaborn_pairplot.png', dpi=100)
    print("Saved: /tmp/seaborn_pairplot.png")
    
    # Count plot
    sns.countplot(data=category_data, x='category', ax=axes[1, 1])
    axes[1, 1].set_title('Count by Category')
    
    plt.tight_layout()
    plt.savefig('/tmp/seaborn_examples.png', dpi=100)
    print("Saved: /tmp/seaborn_examples.png")
    plt.close()


def advanced_visualizations(time_series_df, category_data):
    """Demonstrate advanced visualization techniques"""
    print("Advanced Visualizations:")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Stacked area plot
    pivot_data = category_data.pivot_table(
        index=category_data.index,
        columns='category',
        values='value'
    ).fillna(0)
    
    axes[0, 0].stackplot(pivot_data.columns, pivot_data.T, labels=pivot_data.columns)
    axes[0, 0].set_title('Stacked Area Plot')
    axes[0, 0].legend(loc='upper right')
    
    # Pie chart
    category_counts = category_data['category'].value_counts()
    axes[0, 1].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
    axes[0, 1].set_title('Category Distribution')
    
    # Subplot with multiple y-axes
    color = 'tab:red'
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Value', color=color)
    axes[1, 0].plot(time_series_df['date'], time_series_df['value'], color=color)
    axes[1, 0].tick_params(axis='y', labelcolor=color)
    
    axes2 = axes[1, 0].twinx()
    color = 'tab:blue'
    axes2.set_ylabel('Moving Average', color=color)
    axes2.plot(time_series_df['date'], time_series_df['value'].rolling(window=7).mean(), color=color)
    axes2.tick_params(axis='y', labelcolor=color)
    axes[1, 0].set_title('Time Series with Moving Average')
    
    # Error bar plot
    category_stats = category_data.groupby('category')['value'].agg(['mean', 'std'])
    axes[1, 1].errorbar(category_stats.index, category_stats['mean'], 
                        yerr=category_stats['std'], fmt='o', capsize=5)
    axes[1, 1].set_title('Mean Values with Error Bars')
    axes[1, 1].set_ylabel('Value')
    
    plt.tight_layout()
    plt.savefig('/tmp/advanced_visualizations.png', dpi=100)
    print("Saved: /tmp/advanced_visualizations.png")
    plt.close()


def plotly_examples(time_series_df, category_data):
    """Demonstrate Plotly interactive visualizations"""
    print("Plotly Examples:")
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots
        
        # Interactive line plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_series_df['date'],
            y=time_series_df['value'],
            mode='lines',
            name='Time Series'
        ))
        fig.update_layout(title='Interactive Time Series Plot')
        fig.write_html('/tmp/plotly_timeseries.html')
        print("Saved: /tmp/plotly_timeseries.html")
        
        # Interactive bar chart
        fig_bar = px.bar(
            category_data.groupby('category')['value'].mean().reset_index(),
            x='category',
            y='value',
            title='Average Value by Category'
        )
        fig_bar.write_html('/tmp/plotly_barchart.html')
        print("Saved: /tmp/plotly_barchart.html")
        
        # Interactive scatter plot
        fig_scatter = px.scatter(
            category_data.sample(100),
            x=category_data.sample(100).index,
            y='value',
            color='category',
            title='Scatter Plot by Category'
        )
        fig_scatter.write_html('/tmp/plotly_scatter.html')
        print("Saved: /tmp/plotly_scatter.html")
        
    except ImportError:
        print("Plotly not installed. Install with: pip install plotly")


def main():
    """Main function to demonstrate data visualization"""
    print("Data Visualization Examples")
    print("=" * 50)
    
    # Create sample data
    time_series_df, category_data, corr_data = create_sample_data()
    
    # Matplotlib examples
    matplotlib_examples(time_series_df, category_data, corr_data)
    
    # Seaborn examples
    seaborn_examples(category_data, corr_data)
    
    # Advanced visualizations
    advanced_visualizations(time_series_df, category_data)
    
    # Plotly examples
    plotly_examples(time_series_df, category_data)
    
    print("\n" + "=" * 50)
    print("Data Visualization Key Concepts:")
    print("✓ Matplotlib: Basic plotting and customization")
    print("✓ Seaborn: Statistical visualization")
    print("✓ Plotly: Interactive visualizations")
    print("✓ Various chart types: line, bar, histogram, scatter")
    print("✓ Advanced techniques: heatmaps, pair plots, error bars")
    print("✓ Styling and aesthetics")
    print("\nTo run this script:")
    print("pip install matplotlib seaborn pandas numpy plotly")


if __name__ == "__main__":
    main()