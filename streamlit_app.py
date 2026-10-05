import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, due on October 6th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

global_total_sales = df["Sales"].sum()
global_total_profit = df["Profit"].sum()
global_margin = (global_total_profit / global_total_sales) * 100 if global_total_sales != 0 else 0

selected_cat = st.selectbox(label="1. Select a Category:", options=df["Category"].unique(), index=0, format_func=str, key="category_select_key", help="Filter the entire page analytics by selecting a product category.", on_change=None, args=None, kwargs=None, placeholder="Choose a category...", disabled=False, label_visibility="visible", accept_new_options=False, filter_mode="fuzzy", width="stretch", bind=None, persist_state=None)

sub_options = df[df["Category"] == selected_cat]["Sub_Category"].unique()
selected_subs = st.multiselect(label="2. Select Sub-Categories:", options=sub_options, default=list(sub_options), format_func=str, key="sub_category_select_key", help="Select specific sub-categories to analyze.", on_change=None, args=None, kwargs=None, max_selections=None, placeholder="Choose sub-categories...", disabled=False, label_visibility="visible", accept_new_options=False, filter_mode="fuzzy", select_all=1000, width="stretch", wrap=None, bind=None, persist_state=None)

df_final = df[(df["Category"] == selected_cat) & (df["Sub_Category"].isin(selected_subs))].copy()

if not df_final.empty:
    total_sales_val = df_final["Sales"].sum()
    total_profit_val = df_final["Profit"].sum()
    current_margin = (total_profit_val / total_sales_val) * 100 if total_sales_val != 0 else 0
    margin_delta = current_margin - global_margin

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Sales", value=f"${total_sales_val:,.2f}")
    col2.metric(label="Total Profit", value=f"${total_profit_val:,.2f}")
    col3.metric(label="Overall Profit Margin", value=f"{current_margin:.2f}%", delta=f"{margin_delta:+.2f}% vs Global Avg")

    if "Order_Date" in df_final.columns:
        df_final["Order_Date"] = pd.to_datetime(df_final["Order_Date"])
        sales_trend = df_final.set_index("Order_Date").filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()
    else:
        sales_trend = df_final.filter(items=["Sales"]).groupby(pd.Grouper(freq="ME")).sum()
        
    st.line_chart(sales_trend, y="Sales")
else:
    st.warning("Pick at least one sub-category to view analytics.")


st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
