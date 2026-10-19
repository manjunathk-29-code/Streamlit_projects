
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("Sales Dashboard")

df = pd.DataFrame({
    "Year": np.random.choice([2022, 2023, 2024], 200),
    "Region": np.random.choice(
        ["North", "South", "East", "West"], 200
    ),
    "Product": np.random.choice(["A", "B", "C"], 200),
    "Sales": np.random.randint(1000, 10000, 200)
})


df["Date"] = pd.date_range(
    "2022-01-01", periods=200, freq="D"
)


st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Year",
    df["Year"].unique(),
    default=df["Year"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

product = st.sidebar.multiselect(
    "Product",
    df["Product"].unique(),
    default=df["Product"].unique()
)

date_range = st.sidebar.date_input(
    "Date range",
    value=(
        df["Date"].min().date(),
        df["Date"].max().date()
    )
)


filtered = df[
    (df["Year"].isin(year)) &
    (df["Region"].isin(region)) &
    (df["Product"].isin(product))
]


if len(date_range) == 2:
    filtered = filtered[
        (filtered["Date"] >= pd.Timestamp(date_range[0])) &
        (filtered["Date"] <= pd.Timestamp(date_range[1]))
    ]


c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Sales",
    f"{filtered['Sales'].sum():,}"
)

if not filtered.empty:
    c2.metric(
        "Avg Sales",
        f"{filtered['Sales'].mean():,.0f}"
    )
else:
    c2.metric("Avg Sales", "0")

c3.metric("Records", len(filtered))


st.subheader("Sales by Region")

st.bar_chart(
    filtered.groupby("Region")["Sales"].sum()
)

st.subheader("Sales by Year")

st.line_chart(
    filtered.groupby("Year")["Sales"].sum()
)

st.subheader("Sales by Product")

if not filtered.empty:
    pie_data = (
        filtered.groupby("Product")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        pie_data,
        names="Product",
        values="Sales",
        title="Sales by Product"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
else:
    st.info("No data available for the selected filters.")

st.subheader("Download Filtered Data")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

st.subheader("Filtered Sales Data")
st.dataframe(filtered, use_container_width=True)
