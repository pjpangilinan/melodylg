import streamlit as st
from streamlit_community_navigation_bar import st_navbar
from music import DeezerAPI

st.set_page_config(page_title="Melodylg - For your music needs!", page_icon="logo-square.svg", layout="wide", initial_sidebar_state="collapsed")

pages = ["Dashboard", "Journal", "Search", "Login", "Register"]

styles = {
    "nav": {
        "background-color": "rgb(102, 153, 255)",
        "justify-content": "left",
        "height": "6rem",
    },
    "div": {
        "max-width": "10rem",
    },
    "img": {
        "padding-right": "2rem",
        "height": "5rem",
    },
    "span": {
        "color": "white",
        "padding": "1.2rem",
        "font-size": "1.2rem",
    },
    "active": {
        "background-color": "white",
        "color": "rgb(102, 153, 255)",  
        "font-weight": "600",
        "border-radius": "0.5rem",
        "padding": "0.5rem 1rem",
        "box-shadow": "0 2px 6px rgba(0,0,0,0.1)",
        "transition": "all 0.3s ease-in-out",
    }

}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    styles=styles,
    logo_path="logo-circle.svg",
    options=options
)

st.markdown(
    """
    <style>
    .block-container {
        margin-top: -8rem !important;
    }

    .nav-bottom-line {
        position: fixed;
        top: 6rem; /* Adjust to the height of your navbar */
        left: 0;
        right: 0;
        height: 0.3rem;
        background-color: royalblue;
        z-index: 9999;
    }

    </style>
    <div class="nav-bottom-line"></div>
    """,
    unsafe_allow_html=True
)

api = DeezerAPI()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <h3 style="
            text-align: center;
            background-color: rgb(102, 153, 255);
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            margin-bottom: 20px;">
            Top Songs
        </h3>
        """,
        unsafe_allow_html=True
    )

    top_tracks = api.get_top_tracks(limit=6)

    for track in top_tracks:
        cover_url = track["album"]["cover_medium"]
        title = track["title"]
        artist = track["artist"]["name"]
        streams = track.get("rank", "N/A")
        track_link = track["link"]
        preview_url = track.get("preview")

        with st.container():
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: flex-start;
                            padding: 10px; border: 1px solid #DDD; border-radius: 10px;
                            margin-bottom: 10px; min-height: 120px;">
                    <img src="{cover_url}" width="80" style="border-radius: 5px; margin-right: 15px;">
                    <div style="flex: 1;">
                        <a href="{track_link}" target="_blank" style="text-decoration: none; color: black;">
                            <strong style="font-size: 16px; line-height: 1.2;">{title}</strong>
                        </a><br>
                        <span style="color: gray; font-size: 14px;">{artist}</span><br>
                        <span style="font-size: 12px; color: #555;">Streams: {streams}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if isinstance(preview_url, str) and preview_url.strip().startswith("http"):
            st.audio(preview_url, format="audio/mp3")


with col2:
    st.markdown(
        """
        <h3 style="
            text-align: center;
            background-color: rgb(102, 153, 255);
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            margin-bottom: 20px;">
            Top Albums
        </h3>
        """,
        unsafe_allow_html=True
    )
    top_albums = api.get_top_albums(limit=6)

    for album in top_albums:
        cover_url = album["cover_medium"]
        title = album["title"]
        artist = album["artist"]["name"]
        rank = album.get("position", "N/A") 
        link = album["link"]

        with st.container():
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: flex-start;
                            padding: 10px; border: 1px solid #DDD; border-radius: 10px;
                            margin-bottom: 10px; min-height: 120px;">
                    <img src="{cover_url}" width="80" style="border-radius: 5px; margin-right: 15px;">
                    <div style="flex: 1;">
                        <a href="{link}" target="_blank" style="text-decoration: none; color: black;">
                            <strong style="font-size: 16px; line-height: 1.2;">{title}</strong>
                        </a><br>
                        <span style="color: gray; font-size: 14px;">{artist}</span><br>
                        <span style="font-size: 12px; color: #555;">Rank: {rank}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

with col3:
    st.markdown(
        """
        <h3 style="
            text-align: center;
            background-color: rgb(102, 153, 255);
            color: white;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
            margin-bottom: 20px;">
            Top Artists
        </h3>
        """,
        unsafe_allow_html=True
    )

    top_artists = api.get_top_artists(limit=4)

    for artist in top_artists:
        picture_url = artist["picture_medium"]
        name = artist["name"]
        link = artist["link"]

        try:
            top_track = api.get_artist_top_tracks(artist["id"])[0]
            track_title = top_track["title"]
            preview_url = top_track.get("preview", "")
        except Exception:
            track_title = "Unavailable"
            preview_url = ""

        with st.container():
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: flex-start;
                            padding: 10px; border: 1px solid #DDD; border-radius: 10px;
                            margin-bottom: 10px; min-height: 140px;">
                    <img src="{picture_url}" width="80" style="border-radius: 50%; margin-right: 15px;">
                    <div style="flex: 1;">
                        <a href="{link}" target="_blank" style="text-decoration: none; color: black;">
                            <strong style="font-size: 16px; line-height: 1.2;">{name}</strong>
                        </a><br>
                        <span style="font-size: 14px; color: gray;">Top Track: {track_title}</span><br>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if preview_url:
                st.audio(preview_url, format="audio/mp3")

