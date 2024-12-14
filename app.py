import streamlit as st

with open("data.csv", "r") as f:
    data = f.read()

temperature = data.split(",")[0].strip()
huminity = data.split(",")[1].strip()

if temperature and huminity:
    st.text(f"Temperature: {temperature}")
    st.text(f"Huminity: {huminity}")
else:
    st.text("Error occurred")
