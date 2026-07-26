import base64
from pathlib import Path

import streamlit as st


def render_video_background(video_path: str = "assets/background.mp4") -> None:
    """
    Render a muted looping video as a background.

    Keep the video small. Recommended:
    - MP4 format
    - 5 to 10 seconds loop
    - compressed file size under 5 MB
    """

    path = Path(video_path)

    if not path.exists():
        return

    video_bytes = path.read_bytes()
    encoded_video = base64.b64encode(video_bytes).decode()

    st.markdown(
        f"""
        <video autoplay muted loop playsinline class="video-bg">
            <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
        """,
        unsafe_allow_html=True,
    )