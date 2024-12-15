import streamlit as st
from streamlit_echarts import st_echarts
from raspitemperaturemonitor.db import get_datetime_range, get_last_data, get_data

last_data = get_last_data()
datetime = last_data.datetime.strftime("%Y-%m-%d %H:%M:%S")
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

st.text(f"Updated at {datetime}")
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
        dataset = get_datetime_range(start_datetime, end_datetime)

if dataset:
    options = {
        "tooltip": {"trigger": "axis"},
        "legend": {"data": ["Temperature", "Huminity"]},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [data.datetime.strftime("%Y-%m-%d %H:%M:%S") for data in dataset],
        },
        "yAxis": {
            "type": "value",
            "alignTicks": True,
        },
        "series": [
            {
                "name": "Temperature",
                "type": "line",
                "data": [data.temperature for data in dataset],
                "colorBy": "series",
            },
            {
                "name": "Huminity",
                "type": "line",
                "data": [data.huminity for data in dataset],
                "colorBy": "series",
            },
        ],
        "color": ["#ee6666", "#5470c6"],
    }

    st_echarts(options=options, height=500)

else:
    st.warning("No data")
