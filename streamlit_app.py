import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

selected_cat = st.selectbox(label="1. Select a Category:", options=df["Category"].unique(), index=0, format_func=str, key="category_select_key", help="Filter the entire page analytics by selecting a product category.", on_change=None, args=None, kwargs=None, placeholder="Choose a category...", disabled=False, label_visibility="visible", accept_new_options=False, filter_mode="fuzzy", width="stretch", bind=None, persist_state=None)
selected_subs = st.multiselect(label="2. Select Sub-Categories:", options=df[df["Category"] == selected_cat]["Sub_Category"].unique(), default=list(df[df["Category"] == selected_cat]["Sub_Category"].unique()), format_func=str, key="sub_category_select_key", help="Select specific sub-categories to analyze.", on_change=None, args=None, kwargs=None, max_selections=None, placeholder="Choose sub-categories...", disabled=False, label_visibility="visible", accept_new_options=False, filter_mode="fuzzy", select_all=1000, width="stretch", wrap=None, bind=None, persist_state=None)
df_final = df[(df["Category"] == selected_cat) & (df["Sub_Category"].isin(selected_subs))]

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

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
