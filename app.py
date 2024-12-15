import streamlit as st
from datetime import datetime
from streamlit_echarts import st_echarts
from streamlit_theme import st_theme
from raspitemperaturemonitor.db import get_datetime_range, get_last_data, get_data

theme = st_theme()
if not theme:
    st.stop()

last_data = get_last_data()
updated_at = last_data.datetime.strftime("%Y-%m-%d %H:%M:%S")
temperature = round(last_data.temperature, 1)
huminity = round(last_data.huminity, 1)

st.title(f"Current")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader(f"Temperature🌡")
        st.header(f"{temperature} °C")

with col2:
    with st.container(border=True):
        st.subheader(f"Huminity💧")
        st.header(f"{huminity} %")

st.text(f"Updated at {updated_at}")
st.divider()

st.title("History")

with st.sidebar:
    st.header("Filter")
    start_datetime = st.date_input("Start date", value=None)
    end_datetime = st.date_input("End date", value=None)

    if not start_datetime and not end_datetime:
        dataset = get_data()
        if len(dataset) > 50:
            dataset = dataset[-50:]
    else:
        end_datetime = datetime(
            end_datetime.year, end_datetime.month, end_datetime.day, 23, 59, 59
        )
        dataset = get_datetime_range(start_datetime, end_datetime)

if dataset:
    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {
            "data": ["Temperature", "Huminity"],
            "textStyle": {
                "color": theme["textColor"],
                "fontFamily": theme["font"],
                "fontSize": 14,
            },
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [data.datetime.strftime("%Y-%m-%d %H:%M:%S") for data in dataset],
            "axisLine": {
                "lineStyle": {"color": theme["textColor"]},
            },
        },
        "yAxis": {
            "type": "value",
            "alignTicks": True,
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "color": theme["borderColor"],
                },
            },
        },
        "series": [
            {
                "name": "Temperature",
                "type": "line",
                "data": [round(data.temperature, 1) for data in dataset],
                "colorBy": "series",
            },
            {
                "name": "Huminity",
                "type": "line",
                "data": [round(data.huminity, 1) for data in dataset],
                "colorBy": "series",
            },
        ],
        "color": ["#ee6666", "#5470c6"],
    }

    st_echarts(options=options, height=500)

else:
    st.warning("No data")
