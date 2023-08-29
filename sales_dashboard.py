import streamlit as st
import pandas as pd
import plotly.express as px
#import locale
import calendar
import plotly.io as pio
#locale.setlocale(locale.LC_ALL, 'en_US')

df = pd.read_csv('sales_data.csv')
# Calculate the unique value count for each column
unique_counts = df.nunique()
# Define the data types for each column
dtypes = {}
# Determine the data type for each column
for col in df.columns:
    if col in ['Order Date', 'Ship Date']:
        dtypes[col] = str
    elif df[col].dtype == 'int64':
        dtypes[col] = 'int64'
    elif df[col].dtype == 'float64':
        dtypes[col] = 'float64'
    elif unique_counts[col] / len(df) < 0.5:
        dtypes[col] = 'category'
    else:
        dtypes[col] = str

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


@st.cache_data  # Use caching to improve app performance
def load_data():
    # Load your sales data into a Pandas DataFrame
    df = pd.read_csv('sales_data.csv', dtype=dtypes, parse_dates=['Order Date', 'Ship Date'],dayfirst=True)
    return df

# Load the sales data
df = load_data()
df['Order Month'] = df['Order Date'].dt.month

# Calculate the sales metrics
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
average_order_value = df['Sales'].mean()

sales_by_category = df.groupby('Category')['Sales'].sum().reset_index()
sales_by_subcategory = df.groupby('Sub-Category')['Sales'].sum().reset_index()
sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()
sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()

# Create the Streamlit app
st.title('Interactive Sales Dashboard')

# Format the values as currency
total_sales_formatted = '${:,.2f}'.format(total_sales)
total_profit_formatted = '${:,.2f}'.format(total_profit)
average_order_value_formatted = '${:,.2f}'.format(average_order_value)



# Sidebar for user inputs and selections
st.sidebar.title("Sales Dashboard Options")
#analysis_option = st.sidebar.selectbox("Select Analysis Option", ["OverView", "Top Products", "Sales by Region", "Profit by Category"])



analysis_option = st.sidebar.selectbox("Select Analysis Option", ["Summary", "Top Products", "Sales by Region", "Profit by Category"])
# time_granularity = st.sidebar.selectbox("Select Time Granularity", ["Year", "Month"])

# Perform analysis based on user selection and time granularity
if analysis_option == "Summary":
    st.header("Overall Sales and Profit Summary")
        # Add your code for the overall sales and profit summary by year
#     # Display the sales metrics in three columns
    left_column, middle_column, right_column = st.columns(3)

    # Left column: Total Sales
    with left_column:
        st.subheader('Total Sales')
        st.write(total_sales_formatted)

    # Middle column: Average Order Value
    with middle_column:
        st.subheader('Average Order Value')
        st.write(average_order_value_formatted)

    # Right column: Total Profit
    with right_column:
        st.subheader('Total Profit')
        st.write(total_profit_formatted)


    # # Display the sales data table
    st.subheader("Sales Data")
    st.dataframe(df)

    left_column, right_column = st.columns(2)

    with left_column:

        # Calculate total sales and profits by month
        monthly_sales = df.groupby('Order Month')['Sales'].sum()
        monthly_profits = df.groupby('Order Month')['Profit'].sum()

        # Map the month numbers to month names
        monthly_sales.index = monthly_sales.index.map(lambda x: calendar.month_name[x])
        monthly_profits.index = monthly_profits.index.map(lambda x: calendar.month_name[x])

        # Visualize monthly sales using a bar chart
        fig_sales = px.bar(x=monthly_sales.index, y=monthly_sales,
                        title='Monthly Sales',
                        labels={'x': 'Month', 'y': 'Sales'},
                        template='plotly_white')
        fig_sales.update_layout(width=550)

        st.plotly_chart(fig_sales)


        # Convert Plotly chart to interactive HTML
        #html_bytes = pio.to_html(fig_sales, full_html=True)

        fig_sales.update_layout(width=1000)
        #html_bytes = pio.to_html(fig_sales, full_html=False)
        html_bytes = pio.to_html(fig_sales, full_html=False, include_plotlyjs='cdn')

        # Add a download button for the interactive HTML
        st.download_button(
            label="Download Chart",
            data=html_bytes,
            file_name="monthly_sales_chart.html",
            mime="text/html"
        )



        # # Convert Plotly chart to an image
        # image_bytes = pio.to_image(fig_sales, format='png')

        # # Display the image
        # st.image(image_bytes, caption='Monthly Sales Chart', format='PNG')

        # # Add a download button for the image
        # download_button = st.download_button(
        #     label="Download Chart Image",
        #     data=image_bytes,
        #     file_name="monthly_sales_chart.png",
        #     mime="image/png"
        # )

    with right_column:
        # Visualize monthly profits using a line plot
        fig_profits = px.line(x=monthly_profits.index, y=monthly_profits,
                            title='Monthly Profits',
                            labels={'x': 'Month', 'y': 'Profits'},
                            template='plotly_white')
        fig_profits.update_layout(width=550)
        st.plotly_chart(fig_profits)


    # Display the sales metrics in two columns
    left_column, right_column = st.columns(2)

    # Left column: Sales by Product Category
    with left_column:
        #st.subheader('Sales by Product Category')
        fig_category = px.bar(sales_by_category, x='Category', y='Sales', title='Sales by Product Category')
        st.plotly_chart(fig_category)

    # Right column: Sales by Sub-Category
    with right_column:
        #st.subheader('Sales by Sub-Category')
        fig_subcategory = px.bar(sales_by_subcategory, x='Sub-Category', y='Sales', title='Sales by Sub-Category')
        st.plotly_chart(fig_subcategory)


    # Display the sales metrics in two columns
    left_column, right_column = st.columns(2)

    # Left column: Sales by Region
    with left_column:
        st.subheader('Sales by Region')
        fig_region = px.bar(sales_by_region, x='Region', y='Sales', title='Sales by Region')
        st.plotly_chart(fig_region)

    # Right column: Sales by Customer Segment
    with right_column:
        st.subheader('Sales by Customer Segment')
        fig_segment = px.bar(sales_by_segment, x='Segment', y='Sales', title='Sales by Customer Segment')
        st.plotly_chart(fig_segment)

    # Show a scatter plot of sales and profit
    fig = px.scatter(df, x='Sales', y='Profit', hover_name='Product Name')
    st.plotly_chart(fig)


# Perform analysis based on user selection
elif analysis_option == "Top Products":


    top_n = st.sidebar.number_input("Select Number of Top Products", min_value=1, max_value=10, value=5)

    # Display the sales metrics in two columns
    left_column, right_column = st.columns(2)

    with left_column:
        # Calculate the top selling products
        top_products = df.groupby('Product Name')['Quantity'].sum().nlargest(top_n).reset_index()

        # Create the Plotly bar chart for top selling products
        fig_top_products = px.bar(top_products, x='Product Name', y='Quantity', title='Top Selling Products')

        # Customize the chart appearance
        fig_top_products.update_layout(xaxis_title='Product Name', yaxis_title='Quantity Sold')
        fig_top_products.update_layout(width=550)
        # Display the chart
        st.plotly_chart(fig_top_products)
    with right_column:
        # Calculate the top selling products
        top_products = df.groupby('Product Name')['Profit'].sum().nlargest(top_n).reset_index()

        # Create the Plotly bar chart for top selling products
        fig_top_products = px.bar(top_products, x='Product Name', y='Profit', title='Top Selling Products')

        # Customize the chart appearance
        fig_top_products.update_layout(xaxis_title='Product Name', yaxis_title='Amount of Profits Earned')
        fig_top_products.update_layout(width=550)
        # Display the chart
        st.plotly_chart(fig_top_products)

    # Get unique country names from the data
    country_names = df['Country'].unique()

    # Country selection
    country_selection = st.selectbox("Select Country", country_names)

    # Perform analysis on the selected country
    filtered_data = df[df['Country'] == country_selection]

    left_column, right_column = st.columns(2)

    with left_column:

        product_metrics = filtered_data.groupby('Product Name')['Sales'].sum().reset_index()
        top_products = product_metrics.nlargest(top_n, 'Sales')


        # Visualization: Bar chart of top selling products by sales
        fig = px.bar(top_products, x='Product Name', y='Sales', title=f"Top {top_n} Selling Products in {country_selection}",
                    labels={'Product Name': 'Product Name', 'Sales': 'Sales'})
        st.plotly_chart(fig)

    with right_column:
        product_metrics_profits = filtered_data.groupby('Product Name')['Profit'].sum().reset_index()
        top_products_profits = product_metrics_profits.nlargest(top_n, 'Profit')

        # Visualization: Bar chart of top selling products by sales
        fig = px.bar(top_products_profits, x='Product Name', y='Profit', title=f"Top {top_n} Selling Products in {country_selection}",
                    labels={'Product Name': 'Product Name', 'Profit': 'Profit'})
        st.plotly_chart(fig)


    # with left_column:   
    #     product_metric = df.groupby(['Product Name', 'Order Month'])['Sales'].sum().reset_index()

    #     # Get the top N products based on the chosen metric
    #     top_products = product_metric.groupby('Product Name')['Sales'].sum().nlargest(top_n).index

    #     # Filter the data for the top products
    #     filtered_data = product_metric[product_metric['Product Name'].isin(top_products)]

    #     # Map the month numbers to month names
    #     filtered_data['Order Month'] = filtered_data['Order Month'].apply(lambda x: calendar.month_name[x])

    #     # Visualization: Line chart of top products' sales or profit over time
    #     fig = px.line(filtered_data, x='Order Month', y='Sales', color='Product Name',
    #                 labels={'Order Month': 'Month', 'Sales'.capitalize(): 'Sales'.capitalize()},
    #                 title=f'Top {top_n} Products Sales Trend Over Time')

    #     st.plotly_chart(fig)

    #with right_column:
        

elif analysis_option == "Sales by Region":
    st.header("Sales by Region")

    def plot_top_regions_by_sales(df, region_column, selected_countries=None):
        # Filter data for selected countries or regions
        if selected_countries:
            filtered_data = df[df[region_column].isin(selected_countries)]
        else:
            filtered_data = df

        # Top regions based on sales
        top_regions_sales = filtered_data.groupby(region_column)['Sales'].sum().sort_values(ascending=False)

        # Convert sales values to millions for clearer visualization
        sales_in_millions = top_regions_sales.values / 1e6

        # Create a DataFrame for the visualization
        df_sales = pd.DataFrame({f'{region_column}': top_regions_sales.index, 'Total Sales (Millions)': sales_in_millions})

        # Visualization: Bar chart of top regions by sales using Plotly
        fig = px.bar(df_sales, x=f'{region_column}', y='Total Sales (Millions)', 
                    labels={'x': f'{region_column}', 'y': 'Total Sales (Millions)'},
                    title=f'Top {region_column} by Sales', text='Total Sales (Millions)',
                    hover_data={'Total Sales (Millions)': ':.2f'})

        fig.update_traces(texttemplate='%{text:.2f}m', textposition='outside')

        st.plotly_chart(fig)

    left_column, right_column = st.columns(2)

    with left_column:
        # Get unique countries or regions
        unique_regions = df['Region'].unique()
        # Get top 10 regions or countries by sales
        top_regions_sales = df.groupby('Region')['Sales'].sum().nlargest(10)
        default_selected_regions = top_regions_sales.index.tolist()
        # User selection for countries or regions
        selected_region = st.multiselect('Select Region', unique_regions,default=default_selected_regions)

        # Call the function with user selection
        plot_top_regions_by_sales(df, 'Region', selected_region)

    with right_column:
        unique_countries = df['Country'].unique()
        # Get top 10 regions or countries by sales
        top_countries_sales = df.groupby('Country')['Sales'].sum().nlargest(10)
        default_selected_country = top_countries_sales.index.tolist()
        # User selection for countries or regions
        selected_country = st.multiselect('Select Country', unique_countries,default=default_selected_country)

        plot_top_regions_by_sales(df, 'Country', selected_country)



    left_column, right_column = st.columns(2)

    with left_column:
        sales_by_year = df.groupby('order year')['Sales'].sum().reset_index()

        # Display sales by year
        st.subheader("Sales by Year")
        fig_sales_year = px.bar(sales_by_year, x='order year', y='Sales', title='Sales by Year')
        st.plotly_chart(fig_sales_year)


    # Display sales by region
    st.header("Sales by Region")
    fig_sales_region = px.bar(sales_by_region, x='Region', y='Sales', title='Sales by Region')
    st.plotly_chart(fig_sales_region)


elif analysis_option == "Profit by Category":

    left_column, right_column = st.columns(2)
    with left_column:
        category_performance = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

        # Visualization: Bar chart of product sub-category performance
        fig = px.bar(category_performance, x=category_performance.index, y=category_performance.values,
                    labels={'x': 'Category', 'y': 'Sales'},
                    title='Product Category Performance')

        st.plotly_chart(fig)
    with right_column:
        subcategory_performance = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)

        # Visualization: Bar chart of product sub-category performance
        fig = px.bar(subcategory_performance, x=subcategory_performance.index, y=subcategory_performance.values,
                    labels={'x': 'Sub-Category', 'y': 'Sales'},
                    title='Product Sub-Category Performance')
        st.plotly_chart(fig)


    # Calculate total sales and profits by month and category
    monthly_sales_category = df.groupby(['Order Month', 'Category'])['Sales'].sum().reset_index()
    monthly_profits_category = df.groupby(['Order Month', 'Category'])['Profit'].sum().reset_index()

    # Map the month numbers to month names
    monthly_sales_category['Order Month'] = monthly_sales_category['Order Month'].apply(lambda x: calendar.month_abbr[x])
    monthly_profits_category['Order Month'] = monthly_profits_category['Order Month'].apply(lambda x: calendar.month_abbr[x])

    #for Sub_category
    monthly_sales_sub_category = df.groupby(['Order Month', 'Sub-Category'])['Sales'].sum().reset_index()
    monthly_profits_sub_category = df.groupby(['Order Month', 'Sub-Category'])['Profit'].sum().reset_index()

    # Map the month numbers to month names
    monthly_sales_sub_category['Order Month'] = monthly_sales_sub_category['Order Month'].apply(lambda x: calendar.month_abbr[x])
    monthly_profits_sub_category['Order Month'] = monthly_profits_sub_category['Order Month'].apply(lambda x: calendar.month_abbr[x])

    left_column, right_column = st.columns(2)
    with left_column:

        # Visualize seasonal sales by category using a line plot
        fig_sales_category = px.line(monthly_sales_category, x='Order Month', y='Sales', color='Category',
                                    title='Seasonal Sales by Category',
                                    labels={'Order Month': 'Month', 'Sales': 'Sales', 'Category': 'Category'},
                                    template='plotly_white')
        fig_sales_category.update_layout(width=550)

        st.plotly_chart(fig_sales_category)
    with right_column:


        # Visualize seasonal profits by category using a bar chart
        fig_profits_category = px.bar(monthly_profits_category, x='Order Month', y='Profit', color='Category',
                                    title='Seasonal Profits by Category',
                                    labels={'Order Month': 'Month', 'Profit': 'Profit', 'Category': 'Category'},
                                    template='plotly_white')
        fig_profits_category.update_layout(width=550)
        st.plotly_chart(fig_profits_category)

    left_column, right_column = st.columns(2)
    with left_column:

        # Visualize seasonal sales by category using a line plot
        fig_sales_sub_category = px.line(monthly_sales_sub_category, x='Order Month', y='Sales', color='Sub-Category',
                                    title='Seasonal Sales by Sub-Category',
                                    labels={'Order Month': 'Month', 'Sales': 'Sales', 'Sub-Category': 'Sub-Category'},
                                    template='plotly_white')
        fig_sales_sub_category.update_layout(width=550)

        st.plotly_chart(fig_sales_sub_category)
    with right_column:


        # Visualize seasonal profits by category using a bar chart
        fig_profits_sub_category = px.bar(monthly_profits_sub_category, x='Order Month', y='Profit', color='Sub-Category',
                                    title='Seasonal Profits by Sub-Category',
                                    labels={'Order Month': 'Month', 'Profit': 'Profit', 'Sub-Category': 'Sub-Category'},
                                    template='plotly_white')
        fig_profits_sub_category.update_layout(width=550)
        st.plotly_chart(fig_profits_sub_category)


