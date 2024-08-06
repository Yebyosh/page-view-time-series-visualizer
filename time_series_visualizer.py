import matplotlib.pyplot as plt
from numpy import NaN, nan
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data (filter out days when page views were top 2.5% or bottom 2.5% of dataset)
df = df.loc[(df['value'] >= df['value'].quantile(q=0.025))
            & (df['value'] <= df['value'].quantile(q=0.975))]

#print(df)


# For each chart, make sure to use a copy of the data frame
def draw_line_plot():
    # Draw line plot (use Matplotlib to draw line chart -  title is Daily freeCodeCamp Forum Page Views 5/2016-12/2019, label x axis - Date and y axis - Page Views)
    df_line_chart = df.copy()

    fig, axs = plt.subplots(figsize=(12, 4))
    axs.plot(df_line_chart.index, df_line_chart['value'], color='red')
    axs.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    axs.set_xlabel('Date')
    axs.set_ylabel('Page Views')
    #plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot ( show average daily page views for each month grouped by year)
    df_bar = df.copy()
    df_bar = df_bar.reset_index()
    df_bar['month'] = df_bar['date'].dt.month_name()
    df_bar['year'] = df_bar['date'].dt.year
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)
    #print(df_bar)

    df_fin_bar = df_bar.groupby(['year', 'month']).mean()
    df_fin_bar = df_fin_bar.unstack()
    #print(df_fin_bar)

    # Draw bar plot (legend should show month labels and have a title of Months; x axis = Years, y axis = Average Page Views)
    fig = df_fin_bar.plot(kind='bar').figure
    #plt.subplots(figsize=(12,6)) - cannot include will mess up the labels...
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title='Months', labels=month_order)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn) - two adjacent box plots; show how values distributed within given year or month and how compares over time;  title of first chart = Year-wise Box Plot (Trend);  title of second = Month-wise Box Plot (Seasonality); month labels on bottom start at Jan
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    sns.boxplot(data=df_box, x='year', y='value', ax=axs[0], palette=sns.color_palette(), fliersize=1)
    axs[0].set_xlabel("Year")
    axs[0].set_ylabel("Page Views")
    axs[0].set_title("Year-wise Box Plot (Trend)")

    sns.boxplot(data=df_box, x='month', y='value', ax=axs[1], palette=sns.color_palette("husl", 12), order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fliersize=1)
    axs[1].set_xlabel("Month")
    axs[1].set_ylabel("Page Views")
    axs[1].set_title("Month-wise Box Plot (Seasonality)")

    print(type(fig), type(axs[0]))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
