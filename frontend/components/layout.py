"""Small layout primitives used to keep Streamlit forms/cards visually stable."""

import streamlit as st


def placeholder_space(height: int = 16) -> None:
    """Reserve a predictable vertical slot without rendering visible content."""
    placeholder = st.empty()
    placeholder.markdown(
        f"<div aria-hidden='true' style='height:{int(height)}px;width:100%;'></div>",
        unsafe_allow_html=True,
    )


def reserve_result_slot(height: int = 92, key: str | None = None):
    """Create a fixed-height placeholder for dynamic result/status content."""
    return st.container(height=height, border=False, key=key)
