"""
Header component for the page
"""

import streamlit as st

def render_header():
    """Render the page header"""
    
    # Main title
    st.markdown("""
    <div class="main-header">
        <h1>TradingAgents-CN Stock Analysis Platform</h1>
        <p>A multi-agent LLM-based financial trading decision framework</p>
    </div>
    """, unsafe_allow_html=True)
