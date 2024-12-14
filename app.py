import streamlit as st
from streamlit_echarts import st_echarts
from raspitemperaturemonitor.db import get_last_data, get_data

last_data = get_last_data()
datetime = last_data.datetime.strftime("%Y-%m-%d %H:%M:%S")
temperature = round(last_data.temperature, 1)
huminity = round(last_data.huminity, 1)

st.title(f"Current")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.header(f"Temperature🌡")
        st.subheader(f"{temperature} °C")

with col2:
    with st.container(border=True):
        st.header(f"Huminity💧")
        st.subheader(f"{huminity} %")

st.text(f"Updated at {datetime}")
st.divider()

st.title("Chart")
dataset = get_data()
if len(dataset) > 50:
    dataset = dataset[-50:]


options = {
    "tooltip": {"trigger": "axis"},
    "legend": {"data": ["Temperature", "Huminity"]},
    "xAxis": {
        "type": "category",
        "boundaryGap": False,
        "data": [data.datetime.strftime("%Y-%m-%d %H:%M:%S") for data in dataset],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Temperature",
            "type": "line",
            "data": [data.temperature for data in dataset],
        },
        {
            "name": "Huminity",
            "type": "line",
            "data": [data.huminity for data in dataset],
        },
    ],
}
st_echarts(options=options, height=500)
