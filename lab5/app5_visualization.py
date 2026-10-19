
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Data Visualization")

# --- Sample Data ---
df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Math", "Science", "English"]
)

st.subheader("Built-in Charts")

st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)

st.subheader("Matplotlib Chart")

fig, ax = plt.subplots()
ax.hist(df["Math"], bins=10, color="skyblue")
ax.set_title("Math Score Distribution")
ax.set_xlabel("Math Scores")
ax.set_ylabel("Frequency")

st.pyplot(fig)
plt.close(fig)


st.subheader("Plotly Histogram")

fig = px.histogram(
    df,
    x="Math",
    nbins=10,
    title="Math Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Scatter Chart")

st.scatter_chart(df, x="Math", y="Science")

st.subheader("Average Score")

avg_math = df["Math"].mean()
st.metric("Average Math Score", f"{avg_math:.2f}")
