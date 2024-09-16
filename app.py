import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import LineString, Point

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
    [102.584932, 14.235004], # Near Phnom Penh
    [105.690450, 18.695265]  # Up to Vientiane
]
mekong_line = LineString(mekong_points)
mekong_gdf = gpd.GeoDataFrame({'geometry': [mekong_line]}, crs="EPSG:4326")
highlight_point = gpd.GeoDataFrame({'geometry': [Point
