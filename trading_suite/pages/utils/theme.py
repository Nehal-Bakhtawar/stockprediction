import streamlit as st
import os

def apply_custom_style():
    # Load CSS from the root style.css
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

    # Consistent Sidebar Header
    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚡ Navigation</div>', unsafe_allow_html=True)

def centered_header(title):
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 0.2rem;">
            <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0; padding: 0;">{title}</h1>
        </div>
        """, unsafe_allow_html=True)
