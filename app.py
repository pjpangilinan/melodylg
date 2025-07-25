import streamlit as st
from streamlit_community_navigation_bar import st_navbar
import pages as pg
from auth import init_db

st.set_page_config(page_title="Melodylg - For your music needs!", page_icon="logo-square.svg", layout="wide", initial_sidebar_state="collapsed")

pages = ["Dashboard", "Journal", "Search", "Account"]

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

    .stApp .stNavbar, .nav-list {
        overflow-x: auto !important;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
    }

    .nav-list li {
        display: inline-block !important;
        margin-right: 1rem;
    }

    .nav-list::-webkit-scrollbar {
        display: none;
    }

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

functions = {
    "Home": pg.show_home,
    #"Dashboard": pg.show_dashboard,
    #"Journal": pg.show_journal,
    "Search": pg.show_search,
    "Account": pg.show_login,
}

init_db()

go_to = functions.get(page)
if go_to:
    go_to()