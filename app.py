import base64
import math
import time
from pathlib import Path

import streamlit as st

from backend.QRCodeReader import QRCodeReader


def init_qr_reader():
    return QRCodeReader("backend/pictures/qrcodes.jpg")


searchhistory = 0

content = [
    ("example", (100, 210), "timestamp3"),
    ("example", (100, 220), "timestamp3"),
    ("example", (100, 230), "timestamp3"),
    ("example", (100, 240), "timestamp3"),
]

content_and_positions = [
    ("example", (100, 200), "timestamp1"),
    ("other", (150, 250), "timestamp2"),
    ("example", (300, 400), "timestamp3"),
]


qr_code_reader = init_qr_reader()

# --- Settings ---
map_path = "src/floorplan.png"  # Make sure this path is correct!
img_data = base64.b64encode(Path(map_path).read_bytes()).decode()
dot_radius = 10
map_size = 560  # px

# --- CSS Styling ---
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
        max-width: 100%;
        margin: 0 auto;
    }
    .header-title {
        color: #fff;
        font-size: 2em;
        font-weight: bold;
        letter-spacing: 2px;
    }
    .gap-below-header {
        height: 50px;
    }
    .map-title {
        width: 100%;
        margin-left: 0;
        margin-top: 0.5em;
        text-align: center;
        font-size: 2em;
        font-weight: bold;
    }
    .center-map-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 2em;
    }
    @keyframes blink {
      0%, 100% { opacity: 0; }
      50% { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown(
    """
    <div class="header-outer">
      <div class="header-container">
        <div class="header-title">KLTracking</div>
      </div>
    </div>
    <div class="gap-below-header"></div>
    """,
    unsafe_allow_html=True,
)

# --- Streamlit Search Bar ---
search_query = st.text_input(
    "",  # No label for clean look
    "",
    key="search_bar",
    placeholder="Type to search...",
)

# --- Search Comparison Logic ---

matched_positions = []
if search_query:
    for entry in content:
        if entry[0].lower() == search_query.lower():
            matched_positions.append(entry[1])

# --- Title ---
st.markdown('<div class="map-title">Lager Ansicht</div>', unsafe_allow_html=True)

# --- Centered Map Container ---
st.markdown('<div class="center-map-container">', unsafe_allow_html=True)
overlay_container = st.container()
st.markdown("</div>", unsafe_allow_html=True)


# --- Overlay Fragment: Image and Dots Together ---
@st.fragment(run_every="1s")
def update_overlay():
    t = time.time()
    base = map_size // 2
    r = 240
    # content_and_positions = qr_code_reader.give_box_qr_codes_and_positions()
    content_and_positions = [
        ("example", (100, 200), "timestamp1"),
        ("other", (150, 250), "timestamp2"),
    ]
    coordinates = []
    if len(matched_positions) != 0:
        coordinates = matched_positions
    else:
        for content_and_position in content_and_positions:
            content.append(
                (content_and_position[0], content_and_position[1], time.asctime())
            )
            coordinates.append(content_and_position[1])

    dots_html = "".join(
        f'<div style="position: absolute; left: {x-dot_radius}px; top: {y-dot_radius}px; width: {dot_radius*2}px; height: {dot_radius*2}px; border-radius: 50%; background: red; animation: blink 1s infinite;"></div>'
        for (x, y) in coordinates
    )
    st.markdown(
        f"""
        <div style="position:relative; width:560px; height:560px; border-radius:20px; overflow:hidden; box-shadow:0 2px 12px rgba(0,0,0,0.04);">
            <img style="position:absolute; top:0; left:0; width:560px; height:560px; border-radius:20px; z-index:1; pointer-events:none;" src="data:image/png;base64,{img_data}">
            <div style="position:absolute; top:0; left:0; width:560px; height:560px; z-index:2; pointer-events:none;">{dots_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # matched_positions.clear()


# Place the overlay fragment in the correct container
with overlay_container:
    update_overlay()
