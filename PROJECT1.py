import streamlit as st
import pickle
import plotly.graph_objects as go

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnu_WPCGUt3mdTTcmPF-4GB-JFkTTdL-Jl1g&s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.markdown("<h1 style='white-space: nowrap; text-align: center; color: black;'>AIR POLLUTION CONTROL PREDICTOR</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='color: black; font-size: 16px; text-align: justify;'>
This application allows users to check the pollution level by entering values of different air pollutants like CO, NO2, and PM10.
Based on the inputs, it calculates a pollution score that reflects the overall air quality.
The result is shown as a clear message ranging from "Not Polluted" to "Hazardous".
It helps users easily understand how safe or unsafe the surrounding air is.<br><br>
</div>
""", unsafe_allow_html=True)

# Input form in three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<span style="color:black; font-weight:bold;">Enter CO</span>', unsafe_allow_html=True)
    p = st.number_input("",key="CO")
    st.markdown('<span style="color:black; font-weight:bold;">Enter Ozone</span>', unsafe_allow_html=True)
    g = st.number_input("",key="Ozone")
    st.markdown('<span style="color:black; font-weight:bold;">Enter NO</span>', unsafe_allow_html=True)
    b = st.number_input("",key="NO")

with col2:
    st.markdown('<span style="color:black; font-weight:bold;">Enter NO2</span>', unsafe_allow_html=True)
    s = st.number_input("",key="NO2")
    st.markdown('<span style="color:black; font-weight:bold;">Enter NOX</span>', unsafe_allow_html=True)
    i = st.number_input("",key="NOX")
    st.markdown('<span style="color:black; font-weight:bold;">Enter NH3</span>', unsafe_allow_html=True)
    bmi = st.number_input("",key="NH3")

with col3:
    st.markdown('<span style="color:black; font-weight:bold;">Enter SO2</span>', unsafe_allow_html=True)
    dpf = st.number_input("",key="SO2")
    st.markdown('<span style="color:black; font-weight:bold;">Enter PM2.5</span>', unsafe_allow_html=True)
    a = st.number_input("",key="PM2.5")
    st.markdown('<span style="color:black; font-weight:bold;">Enter PM10</span>', unsafe_allow_html=True)
    PM = st.number_input("",key="PM10")

# Load model and scaler
model = pickle.load(open("PROJECT1.pkl", "rb"))
sd = pickle.load(open("scale.pkl", "rb"))

# Prediction logic
if st.button('Predict'):
    input = [[p, g, b, s, i, bmi, dpf, a, PM]]
    scaled = sd.transform(input)
    result = float(model.predict(scaled)[0])  # Ensure float for plotting

    # AQI category display
    if result > 300:
        st.markdown("<h3 style='color: darkred;'>HAZARDOUS</h3>", unsafe_allow_html=True)
    elif result > 200:
        st.markdown("<h3 style='color: red;'>Very Unhealthy</h3>", unsafe_allow_html=True)
    elif result > 150:
        st.markdown("<h3 style='color: orange;'>Unhealthy</h3>", unsafe_allow_html=True)
    elif result > 100:
        st.markdown("<h3 style='color: gold;'>Unhealthy for Sensitive Group</h3>", unsafe_allow_html=True)
    elif result > 50:
        st.markdown("<h3 style='color: blue;'>Moderate</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: green;'>Not Polluted</h3>", unsafe_allow_html=True)

    # Plotly AQI Scale Chart
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=result,
        title={'text': "Air Quality Index (AQI)", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 500]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 50], 'color': "green"},
                {'range': [51, 100], 'color': "blue"},
                {'range': [101, 150], 'color': "gold"},
                {'range': [151, 200], 'color': "orange"},
                {'range': [201, 300], 'color': "red"},
                {'range': [301, 500], 'color': "darkred"}
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)
