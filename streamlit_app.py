import streamlit as st
import pandas as pd

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df = df.dropna(subset=["Order_Date"]).copy()
st.dataframe(df)

st.bar_chart(df, x="Category", y="Sales")

category_summary = df.groupby("Category", as_index=False).sum(numeric_only=True)
st.dataframe(category_summary)
st.bar_chart(category_summary, x="Category", y="Sales", color="#04f")

# Aggregating by time
df.set_index("Order_Date", inplace=True)
sales_by_month = df[["Sales"]].groupby(pd.Grouper(freq="M")).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month)

st.write("## Your additions")

categories = sorted(df["Category"].dropna().unique())
selected_category = st.selectbox("Select a Category", categories)

category_df = df[df["Category"] == selected_category].copy()
subcategories = sorted(category_df["Sub_Category"].dropna().unique())
selected_subcategories = st.multiselect(
    "Select Sub Categories",
    subcategories,
    default=subcategories,
)

filtered_df = category_df[category_df["Sub_Category"].isin(selected_subcategories)].copy()

if not filtered_df.empty:
    sales_trend = (
        filtered_df[["Sales"]]
        .groupby(pd.Grouper(freq="M"))
        .sum()
    )

    st.write(f"### Sales trend for {selected_category}")
    st.line_chart(sales_trend)

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_revenue = filtered_df["Sales"].sum()

    overall_profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0.0
    overall_average_profit_margin = (
        (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() else 0.0
    )
    margin_delta = overall_profit_margin - overall_average_profit_margin

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Profit", f"${total_profit:,.2f}")
    with col3:
        st.metric(
            "Overall Profit Margin (%)",
            f"{overall_profit_margin:.2f}%",
            delta=f"{margin_delta:.2f}% vs overall avg",
        )
else:
    st.info("Please select at least one subcategory.")
