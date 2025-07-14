import pandas as pd
import plotly.express as px
import re

# Load data
data_sales = pd.read_csv('sales_data.csv')
data_sales['date'] = pd.to_datetime(data_sales['date'])
data_customer = pd.read_csv('customer_data.csv')
data_customer['date'] = pd.to_datetime(data_customer['date'])

# NLP Parser
def parse_query(query):
    query = query.lower()
    result = {'action': None, 'column': None, 'group_by': None, 'visualize': False, 'dataset': 'sales'}
    if 'customer' in query:
        result['dataset'] = 'customer'
    if 'total' in query or 'sum' in query:
        result['action'] = 'sum'
    elif 'trend' in query or 'over time' in query:
        result['action'] = 'trend'
    elif 'highest' in query or 'top' in query:
        result['action'] = 'max'
    if 'sales' in query:
        result['column'] = 'sales'
    if 'region' in query:
        result['group_by'] = 'region'
    if 'date' in query or 'time' in query:
        result['group_by'] = 'date'
    if 'product' in query:
        result['group_by'] = 'product'
    if 'plot' in query or 'chart' in query:
        result['visualize'] = True
    return result

# Process Query
def process_query(query, data_sales, data_customer):
    parsed = parse_query(query)
    action = parsed['action']
    column = parsed['column']
    group_by = parsed['group_by']
    visualize = parsed['visualize']
    data = data_customer if parsed['dataset'] == 'customer' else data_sales

    if not column or not action:
        return "Sorry, I couldn't understand the query. Please specify what to analyze (e.g., sales)."

    if action == 'sum' and group_by:
        result = data.groupby(group_by)[column].sum().reset_index()
        text = f"Total {column} by {group_by}:\n{result.to_string(index=False)}"
        if visualize:
            fig = px.bar(result, x=group_by, y=column, title=f"Total {column} by {group_by}")
            return text, fig
        return text
    elif action == 'trend' and group_by == 'date':
        result = data.groupby('date')[column].sum().reset_index()
        text = f"Trend of {column} over time."
        if visualize:
            fig = px.line(result, x='date', y=column, title=f"{column} Trend Over Time")
            return text, fig
        return text
    elif action == 'max' and group_by:
        result = data.groupby(group_by)[column].sum().idxmax()
        text = f"Highest {column} in {group_by}: {result}"
        return text
    return "Unsupported query type."

# Example Usage
if __name__ == "__main__":
    query = "Plot a bar chart of total sales by region"
    output = process_query(query, data_sales, data_customer)
    if isinstance(output, tuple):
        print(output[0])
        output[1].show()
    else:
        print(output)
