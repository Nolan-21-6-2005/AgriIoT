from pathlib import Path

import streamlit as st


def _load_css() -> str:
    css_path = Path(__file__).resolve().parents[1] / "assets" / "style.css"
    return css_path.read_text(encoding="utf-8")


def apply_styles() -> None:
    st.markdown(f"<style>{_load_css()}</style>", unsafe_allow_html=True)
