import streamlit as st
from music import DeezerAPI
from auth import login_user, register_user, reset_password
from streamlit_extras.stylable_container import stylable_container

api = DeezerAPI()

def show_home():
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

def show_search():
    st.set_page_config(page_title="Search | Melodylg", layout="centered")

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Search", placeholder="Try 'Taylor Swift' or 'After Hours'")
    with col2:
        search_type = st.selectbox("Search Type", ["Track", "Album", "Artist"])

    def render_card(img, title, subtitle, link, circle=False):
        radius = "50%" if circle else "10px"
        return f"""
            <div style="display: flex; align-items: center; padding: 15px;
                        border: 1px solid #ddd; border-radius: 12px; background-color: #f9f9f9;
                        margin-bottom: 10px;">
                <img src="{img}" width="80" 
                    style="border-radius: {radius}; margin-right: 15px;">
                <div>
                    <a href="{link}" target="_blank" 
                    style="text-decoration: none; color: #222;">
                        <strong style="font-size: 16px;">{title}</strong>
                    </a><br>
                    <span style="color: #666;">{subtitle}</span>
                </div>
            </div>
        """

    if query.strip():
        if search_type == "Track":
            results = api.search_tracks(query)
            if results:
                st.markdown("### 🎵 Tracks Found", unsafe_allow_html=True)
                for track in results[:5]:
                    st.markdown(render_card(
                        img=track['album']['cover_medium'],
                        title=track['title'],
                        subtitle=track['artist']['name'],
                        link=track['link']
                    ), unsafe_allow_html=True)

                    if track.get("preview"):
                        st.audio(track["preview"], format="audio/mp3")
            else:
                st.warning("No tracks found.")

        elif search_type == "Album":
            results = api.search_albums(query)
            if results:
                st.markdown("### 💿 Albums Found", unsafe_allow_html=True)
                for album in results[:5]:
                    st.markdown(render_card(
                        img=album['cover_medium'],
                        title=album['title'],
                        subtitle=album['artist']['name'],
                        link=album['link']
                    ), unsafe_allow_html=True)
            else:
                st.warning("No albums found.")

        elif search_type == "Artist":
            results = api.search_artists(query)
            if results:
                st.markdown("### 🎤 Artists Found", unsafe_allow_html=True)
                for artist in results[:5]:
                    st.markdown(render_card(
                        img=artist['picture_medium'],
                        title=artist['name'],
                        subtitle="",
                        link=artist['link'],
                        circle=True
                    ), unsafe_allow_html=True)

                    try:
                        top_track = api.get_artist_top_tracks(artist["id"])[0]
                        if top_track.get("preview"):
                            st.markdown(f"Top Track: *{top_track['title']}*", unsafe_allow_html=True)
                            st.audio(top_track["preview"], format="audio/mp3")
                    except:
                        st.info("No top track preview.")
            else:
                st.warning("No artists found.")

def show_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        }

        .auth-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: rgb(40, 40, 90);
            margin-bottom: 2rem;
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        }

        .auth-tab button {
            width: 100%;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.7rem 0;
            border-radius: 10px;
            border: none;
            background-color: #e0e0e0;
            color: #333;
            transition: all 0.3s ease;
        }

        .auth-tab button:hover {
            background-color: #d5d5d5;
        }

        .auth-tab .active {
            background-color: royalblue !important;
            color: white !important;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > textarea {
            border-radius: 8px !important;
        }

        .stButton>button {
            width: 100%;
            background-color: royalblue;
            color: white;
            padding: 0.65rem 0;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            transition: background-color 0.3s ease;
            margin-top: 1.2rem;
        }

        .stButton>button:hover {
            background-color: #4169e1;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.success(f"You're already logged in as **{st.session_state.username}**")
        return

    with stylable_container(
        key="auth_box",
        css_styles="""
            {
                background-color: #fdfdfd;
                padding: 3rem 2.5rem;
                border-radius: 20px;
                max-width: 550px;
                margin: 4rem auto;
                box-shadow: 0 10px 28px rgba(0, 0, 0, 0.1);
                margin-top: 0rem !important;
            }
        """
    ):
        st.markdown('<div class="auth-title">Melodylg</div>', unsafe_allow_html=True)

        tab_cols = st.columns(3)
        modes = [("login", "Login"), ("register", "Register"), ("forgot", "Forgot Password")]

        for i, (key, label) in enumerate(modes):
            is_active = st.session_state.auth_mode == key
            button_style = "auth-tab active" if is_active else "auth-tab"
            with tab_cols[i]:
                if st.button(label, key=f"mode_{key}"):
                    st.session_state.auth_mode = key

                # Add invisible class div for styling hooks
                st.markdown(f'<div class="{button_style}" style="display:none;"></div>', unsafe_allow_html=True)

        # ── Mode-specific Form ──
        mode = st.session_state.auth_mode

        if mode == "login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                else:
                    st.error("❌ Invalid username or password.")

        elif mode == "register":
            username = st.text_input("Create Username")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if password != confirm:
                    st.warning("⚠️ Passwords do not match.")
                elif register_user(username, password):
                    st.success("✅ Registered! You can now log in.")
                    st.session_state.auth_mode = "login"
                else:
                    st.error("⚠️ Username already exists.")

        elif mode == "forgot":
            username = st.text_input("Username")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Reset Password"):
                if reset_password(username, new_pass):
                    st.success("🔁 Password reset! You can now log in.")
                    st.session_state.auth_mode = "login"
                else:
                    st.error("❌ Username not found.")

def show_register():
    ...