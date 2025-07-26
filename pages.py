import streamlit as st
from music import DeezerAPI
from auth import register_user, reset_password, user_exists, is_correct_password, is_strong_password, get_journal_entries, add_journal_entry, delete_journal_entry, update_journal_entry
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime

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
        st.success(f"✅ You are logged in as **{st.session_state.username}**")

        if st.button("🔓 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("You have been logged out.")
            st.rerun()
        st.stop()

    with stylable_container(
        key="auth_box",
        css_styles="""
            {
                background-color: #fdfdfd;
                padding: 3rem 2.5rem;
                border-radius: 20px;
                max-width: 600px;
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

        st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

        mode = st.session_state.auth_mode

        if mode == "login":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if not user_exists(username):
                    st.error("❌ Username not found.")
                elif not is_correct_password(username, password):
                    st.error("❌ Incorrect password.")
                else:
                    st.success("✅ Login successful!")
                    st.session_state.logged_in = True
                    st.session_state.username = username

        elif mode == "register":
            username = st.text_input("Create Username")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if not username or not password or not confirm:
                    st.warning("⚠️ All fields are required.")
                elif user_exists(username):
                    st.error("🚫 That username is already taken. Try another.")
                elif password != confirm:
                    st.warning("⚠️ Passwords do not match.")
                elif not is_strong_password(password):
                    st.error("""
                        ❌ Weak password.
                        Password must be at least 8 characters long and contain:
                        - ✅ Uppercase letters  
                        - ✅ Lowercase letters  
                        - ✅ Numbers  
                        - ✅ Special characters (e.g. !@#&)
                    """)
                else:
                    success = register_user(username, password)
                    if success:
                        st.success("✅ Account created! You can now log in.")
                        st.session_state.auth_mode = "login"
                    else:
                        st.error("❌ Something went wrong while creating the account. Please try again.")

        elif mode == "forgot":
            username = st.text_input("Username")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Reset Password"):
                if not user_exists(username):
                    st.error("❌ Username not found.")
                else:
                    reset_password(username, new_pass)
                    st.success("✅ Password reset! You can now log in.")
                    st.session_state.auth_mode = "login"

def icon_card_button(label, key, action_callback):
    with stylable_container(
        key=f"icon_card_{key}",
        css_styles="""
            button {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0.5rem auto;
                margin-top: -0.5rem;
                height: 2rem !important;
                width: 100% !important;
                padding: 0.5rem !important;
                border-radius: 1.2rem !important;
                border: 2px solid #e0e0e0 !important;
                background-color: white !important;
                transition: transform 0.2s ease, background-color 0.2s ease;
                font-size: 1rem;
            }
            button:hover {
                background-color: #f0f0f0 !important;
                transform: scale(1.05);
                border-color: #aaaaaa !important;
                color: #067dfc !important;
            }
        """
    ):
        if st.button(label, key=key):
            action_callback()

def set_mode(mode):
    st.session_state.mode = mode
    st.session_state.editing_entry = None

def show_mode_buttons():
    mode_col1, mode_col2, mode_col3 = st.columns([1, 1, 1])
    with mode_col1:
        icon_card_button("View Mode", "btn_view_mode", lambda: set_mode("view"))
    with mode_col2:
        icon_card_button("Edit Mode", "btn_edit_mode", lambda: set_mode("edit"))
    with mode_col3:
        icon_card_button("Delete Mode", "btn_delete_mode", lambda: set_mode("delete"))

def show_journal():
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("Please log in to access your journal")
        st.stop()

    for key, default in {
        "editing_entry": None,
        "search_results": [],
        "search_query": "",
        "search_type": "Track",
        "new_notes": {},
        "force_refresh": False,
        "mode": "view"
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = get_journal_entries(st.session_state.username)

    if st.session_state.get("force_refresh"):
        st.session_state.journal_entries = get_journal_entries(st.session_state.username)
        st.session_state.force_refresh = False

    col1, col2 = st.columns([1.1, 2])

    with col1:
        st.markdown("### Search Music")
        with stylable_container(key="search_box", css_styles="""
            {background-color: #fafafa; padding: 1.5rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);}
        """):
            search_type = st.selectbox("Search by", ["Track", "Artist", "Album"])
            query = st.text_input("Type to search", placeholder="e.g. Taylor Swift, Red, After Hours")

            if query:
                try:
                    if search_type == "Track":
                        st.session_state.search_results = api.search_tracks(query)
                    elif search_type == "Artist":
                        st.session_state.search_results = api.search_artists(query)
                    elif search_type == "Album":
                        st.session_state.search_results = api.search_albums(query)
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
            else:
                st.session_state.search_results = []

            for item in st.session_state.search_results:
                with stylable_container(key=f"card_{item['id']}", css_styles="""
                    {margin-top: 1rem; background-color: #ffffff; border: 1px solid #ddd; padding: 1rem; border-radius: 12px;}
                """):
                    title = item.get("title") or item.get("name")
                    artist = item.get("artist", {}).get("name", "Unknown")
                    album = item.get("album", {}).get("title", "Unknown") if "album" in item else title

                    row = st.columns([1, 3])
                    with row[0]:
                        if item.get("album", {}).get("cover_medium") or item.get("picture_medium"):
                            st.image(item.get("album", {}).get("cover_medium", "") or item.get("picture_medium", ""), width=100)
                    with row[1]:
                        st.markdown(f"**{title}**")
                        st.markdown(f"{artist} | {album}")

                    st.markdown("<div style='margin-top: 0.5rem'></div>", unsafe_allow_html=True)

                    if item.get("preview"):
                        st.audio(item["preview"])

                    notes = st.text_area("Notes", key=f"note_{item['id']}", label_visibility="collapsed", placeholder="Write your thoughts...")

                    icon_card_button("Add to Journal", f"add_{item['id']}", lambda item=item, title=title, artist=artist, album=album, notes=notes: add_to_journal(item, title, artist, album, notes))

    with col2:
        st.markdown("### Your Journal")
        show_mode_buttons()

        if not st.session_state.journal_entries:
            st.info("No journal entries found.")

        for entry in st.session_state.journal_entries:
            with stylable_container(key=f"entry_{entry['id']}", css_styles="""
                {background-color: #ffffff; padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 3px 10px rgba(0,0,0,0.08);}
            """):
                row = st.columns([1, 5])
                with row[0]:
                    if entry.get("image"):
                        st.image(entry["image"], width=120)
                with row[1]:
                    st.markdown(f"**{entry['song_title']}**")
                    st.markdown(f"{entry['artist_name']} | {entry['album_title']} | {entry['date_added']}")

                    if entry['preview_url']:
                        st.audio(entry['preview_url'])
                    
                        st.markdown("<div style='margin-top: 1.5rem'></div>", unsafe_allow_html=True)

                if st.session_state.mode == "edit":
                    new_notes = st.text_area("Edit Notes", value=entry["notes"], key=f"edit_{entry['id']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        icon_card_button("Save Changes", f"save_{entry['id']}", lambda: save_entry(entry['id'], new_notes))
                    with col2:
                        icon_card_button("Cancel", f"cancel_{entry['id']}", lambda: set_mode("view"))
                elif st.session_state.mode == "delete":
                    icon_card_button("Delete", f"del_{entry['id']}", lambda: delete_entry(entry['id']))
                else:
                    if entry['notes']:
                        st.markdown(f"**Notes:**\n{entry['notes']}")


def add_to_journal(item, title, artist, album, notes):
    add_journal_entry(
        username=st.session_state.username,
        song_title=title,
        artist_name=artist,
        album_title=album,
        preview_url=item.get("preview", ""),
        notes=notes,
        date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        image=item.get("album", {}).get("cover_medium", "") or item.get("picture_medium", "")
    )
    st.session_state.force_refresh = True
    st.success("Entry added to journal!")

def save_entry(entry_id, notes):
    update_journal_entry(entry_id, notes)
    set_mode("view")
    st.session_state.force_refresh = True
    st.success("Changes saved!")

def delete_entry(entry_id):
    delete_journal_entry(entry_id)
    st.session_state.force_refresh = True
    set_mode("view")
    st.success("Entry deleted!")

def edit_entry(entry_id):
    st.session_state.editing_entry = entry_id

