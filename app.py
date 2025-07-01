import base64
import time
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from backend.QRCodeReader import QRCodeReader

# Convert image to base64
map_path = "src/map.png"  # Make sure this path is correct!
img_data = base64.b64encode(Path(map_path).read_bytes()).decode()

dot_radius = 10


@st.cache_resource  # Cache the backend instance
def init_qr_reader():
    return QRCodeReader("backend/pictures/qrcodes.jpg")


qr_code_reader = init_qr_reader()

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, limit=None, key="qrcode_refresh")


# Header and style
st.markdown(
    """
<style>
.header-outer {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    background: #222;
    z-index: 1000;
    box-sizing: border-box;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em 2em 1em 2em;
    max-width: 1800px;
    margin: 0 auto;
}
.header-title {
    color: #fff;
    font-size: 2em;
    font-weight: bold;
    letter-spacing: 2px;
}
.header-separator {
    width: 1px;
    height: 2.5em;
    background: #444;
    margin: 0 2em;
    border-radius: 2px;
    opacity: 0.7;
}
.header-search input {
    padding: 0.5em 1em;
    border-radius: 6px;
    border: none;
    font-size: 1em;
    width: 220px;
}
.gap-below-header {
    height: 2.5em;
}
.map-outer {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    box-sizing: border-box;
    padding-left: 32px;
    padding-top: 0;
}
.left-map-container {
    position: relative;
    width: 100%;
    margin-left: 0;
    margin-right: 0;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.left-map-container img {
    width: 560px;
    height: 560px;
    display: block;
    border-radius: 20px;
}
.map-title {
    width: 800px;
    margin-left: 0;
    margin-top: 0.5em;
    text-align: center;
    font-size: 2em;
    font-weight: bold;
}
</style>
<div class="header-outer">
  <div class="header-container">
    <div class="header-title">CrazyCamera</div>
    <div class="header-separator"></div>
    <div class="header-search">
      <form action="" method="get">
        <input name="search_query" type="text" placeholder="Type to search..." value="">
      </form>
    </div>
  </div>
</div>
<div class="gap-below-header"></div>
""",
    unsafe_allow_html=True,
)
# Get updated coordinates
coordinates = qr_code_reader.give_box_qr_codes_and_positions()
# coordinates = {(0, 0), (0, 540), (540, 540), (540, 0)}
# Generate updated dots HTML
dots_html = "".join(
    f'<div style="position: absolute; left: {x}px; top: {y}px; width: {dot_radius*2}px; height: {dot_radius*2}px; border-radius: 50%; background: red; animation: blink 1s infinite;"></div>'
    for (x, y) in coordinates
)
#
# Add this near your map rendering code
dots_container = st.empty()
# Update only the dots container
with dots_container:
    st.markdown(
        f"""
        <div class="map-outer">
          <div class="left-map-container" style="position: relative;">
            <img src="data:image/png;base64,{img_data}">
            {dots_html}
          </div>
          <div class="map-title">Lager Ansicht</div>
        </div>
        <style>
        @keyframes blink {{
          0%, 100% {{ opacity: 0; }}
          50% {{ opacity: 1; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
