import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pydeck as pdk
from shapely.geometry import LineString

# Set Streamlit page configuration
st.set_page_config(page_title="Greenmovement", layout="centered")

# Load and display the logo in the sidebar
logo = "logo.jpg"
st.sidebar.image(logo, use_column_width=True)

st.sidebar.title("Configuration")
input_password = st.sidebar.text_input("Enter Password", type="password")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

correct_password = "greenmovement"
if input_password != correct_password:
    st.sidebar.error("Incorrect password. Access denied.")
    st.stop()

model_options = {
    "Llama 70B Versatile": "llama-3.1-70b-versatile",
    "Llama 8B Instant": "llama-3.1-8b-instant",
    "Llama Guard 8B": "llama-guard-3-8b"
}
selected_model = st.sidebar.selectbox("Select Model", list(model_options.keys()))
api_key = st.secrets["groq"]["api_key"]

# Manual data creation for Mekong River
mekong_points = [
    (34.2044, 109.3359), # Example points, replace with actual coordinates
    (32.2044, 107.3359),
    # Add more points to accurately represent the Mekong River
]
mekong_line = LineString(mekong_points)
mekong_gdf = gpd.GeoDataFrame(geometry=[mekong_line], crs="EPSG:4326")

# Display the map with the Mekong River
st.subheader("Mekong River Map")
layer = pdk.Layer(
    "PathLayer",
    mekong_gdf,
    get_path="coordinates",
    get_width=5000,
    get_color=[255, 100, 100],
    pickable=True,
)
view_state = pdk.ViewState(
    latitude=mekong_gdf.geometry.centroid.y.mean(),
    longitude=mekong_gdf.geometry.centroid.x.mean(),
    zoom=5,
    pitch=50,
)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Continue with the rest of the code for data handling and UI components
