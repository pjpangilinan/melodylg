import os
import streamlit as st
from streamlit_community_navigation_bar import st_navbar

st.set_page_config(page_title="Melodylg - For your music needs!", page_icon="logo-square.svg", initial_sidebar_state="collapsed")

pages = ["Login", "Register"]

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
        "padding": "1rem",
        "font-size": "1.2rem",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "2.5rem",
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