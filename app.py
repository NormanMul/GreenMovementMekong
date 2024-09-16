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
highlight_point = gpd.GeoDataFrame({'geometry': [Point(102.6006, 17.9667)]}, crs="EPSG:4326")  # Vientiane

# Convert GeoDataFrames to json for PyDeck
mekong_json = mekong_gdf.__geo_interface__
highlight_json = highlight_point.__geo_interface__

# Display the map with the Mekong River
st.subheader("Mekong River Map")
path_layer = pdk.Layer(
    type="PathLayer",
    data=mekong_json,
    get_path="coordinates",
    width_scale=20,
    get_color=[200, 30, 0, 160],
    get_width=5,
    pickable=True
)
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=highlight_json,
    get_position="coordinates",
    get_color=[255, 0, 0, 160],  # Red color
    get_radius=150000,  # Adjusted for better visibility
    pickable=True
)

view_state = pdk.ViewState(
    latitude=16.047079,  # Centered on Laos
    longitude=105.870030,  # Centered on Laos
    zoom=5,
    pitch=50,
)
st.pydeck_chart(pdk.Deck(
    layers=[path_layer, scatter_layer],
    initial_view_state=view_state
))

# Legend
st.write("### Legend")
st.write("🔴 - Specific Area of Interest on the Mekong River")

# Load and display the river image
river_image = "River.jpg"
st.image(river_image, caption="Mekong River", use_column_width=True)

# Function to handle response generation
def generate_response(prompt):
    from groq import Groq  # Assuming Groq is a correct import
    client = Groq(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model_options[selected_model],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"An error occurred
