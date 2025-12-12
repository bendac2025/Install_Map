import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Global LED Portfolio")

# --- 1. Load Data ---
@st.cache_data
def load_data():
    # Load the CSV file
    try:
        df = pd.read_csv('projects.csv')
        return df
    except FileNotFoundError:
        st.error("projects.csv not found. Please ensure the file is in the directory.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    
    # --- 2. Sidebar Filters ---
    st.sidebar.header("Portfolio Filters")
    
    # Get unique categories for the multiselect
    all_categories = df['Category'].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "Filter by Project Type",
        options=all_categories,
        default=all_categories # Select all by default
    )
    
    # Filter the dataframe based on selection
    filtered_df = df[df['Category'].isin(selected_categories)]
    
    # --- 3. Main Content ---
    st.title("🌍 Global LED Installation Map")
    st.markdown(f"Showing **{len(filtered_df)}** projects.")

    # Create the Folium Map
    # Center map roughly on a global view or the average of coordinates
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

    # Loop through the filtered data to add markers
    for index, row in filtered_df.iterrows():
        # Create HTML for the popup
        # We use simple HTML/CSS to style the image and text inside the bubble
        html = f"""
        <div style="font-family: sans-serif; width: 200px;">
            <h4 style="margin-bottom: 5px;">{row['Project Name']}</h4>
            <span style="background-color: #333; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 10px;">
                {row['Category']}
            </span>
            <p style="margin: 5px 0;"><b>Screen Size:</b> {row['Screen Size']}</p>
            <img src="{row['Image URL']}" style="width: 100%; border-radius: 5px; margin-top: 5px;">
        </div>
        """
        
        # Create an IFrame to hold the HTML content safely
        iframe = folium.IFrame(html, width=220, height=250)
        popup = folium.Popup(iframe, max_width=250)

        # Add Marker
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            tooltip=row['Project Name'],
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # --- 4. Render Map ---
    st_folium(m, width="100%", height=600)
    
    # Optional: Show raw data below map
    with st.expander("View Raw Project Data"):
        st.dataframe(filtered_df)

else:
    st.warning("No data to display. Please create the projects.csv file.")
