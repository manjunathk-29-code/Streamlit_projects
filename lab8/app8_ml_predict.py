
import streamlit as st
import joblib
import numpy as np

st.title("Iris Flower Prediction")

model = joblib.load("model.pkl")

classes = ["Setosa", "Versicolor", "Virginica"]

with st.form("prediction_form"):
    sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)
    sw = st.slider("Sepal Width", 2.0, 4.5, 3.5)
    pl = st.slider("Petal Length", 1.0, 7.0, 1.4)
    pw = st.slider("Petal Width", 0.1, 2.5, 0.2)

    submit = st.form_submit_button("Predict")

if submit:
    features = np.array([[sl, sw, pl, pw]])

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    st.success(f"Prediction: **{classes[pred]}**")

    confidence = max(proba) * 100
    st.metric("Confidence", f"{confidence:.1f}%")
