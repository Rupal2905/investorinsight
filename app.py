import streamlit as st
import pandas as pd
from pathlib import Path
import base64

# Configure page
st.set_page_config(
    page_title="Stock Portfolio Manager",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_theme(theme):
    """Apply theme styles"""
    if theme == 'dark':
        st.markdown("""
            <style>
                :root {
                    --primary-color: #2962FF;
                    --background-color: #0A1929;
                    --secondary-background-color: #132F4C;
                    --text-color: #FFFFFF;
                    --accent-color: #3399FF;
                }
                .stApp {
                    background: linear-gradient(to bottom right, var(--background-color), #1A1A2E);
                    color: var(--text-color);
                }
                /* Card styles */
                div[data-testid="stForm"] {
                    border-radius: 10px;
                    padding: 2rem;
                    background: rgba(255, 255, 255, 0.05);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                /* Data display styles */
                div[data-testid="stDataFrame"] {
                    background: rgba(255, 255, 255, 0.03);
                    border-radius: 10px;
                    padding: 1rem;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
                /* Navigation bar styles */
                .nav-container {
                    background: linear-gradient(to right, rgba(41, 98, 255, 0.1), rgba(0, 0, 0, 0));
                    padding: 1rem 2rem;
                    margin: -1rem -1rem 1rem -1rem;
                    position: relative;
                    z-index: 100;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                }
                .nav-links {
                    display: flex;
                    gap: 1.5rem;
                    align-items: center;
                }
                .nav-link {
                    color: var(--text-color);
                    text-decoration: none;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    font-weight: 600;
                    position: relative;
                    letter-spacing: 0.3px;
                    background: rgba(255, 255, 255, 0.05);
                }
                .nav-link:hover {
                    background: rgba(255, 255, 255, 0.1);
                    transform: translateY(-2px);
                }
                .nav-link.active {
                    background: var(--accent-color);
                    color: white;
                }
                /* Theme toggle button */
                .stButton button {
                    background: rgba(255, 255, 255, 0.1);
                    border: none;
                    color: var(--text-color);
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 600;
                    backdrop-filter: blur(5px);
                }
                .stButton button:hover {
                    background: rgba(255, 255, 255, 0.2);
                    transform: translateY(-2px);
                }
                /* Success message styling */
                div[data-testid="stAlert"] {
                    background: rgba(46, 125, 50, 0.1);
                    border-color: rgba(46, 125, 50, 0.2);
                    color: #66BB6A;
                    border-radius: 8px;
                    padding: 1rem;
                    margin: 1rem 0;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                :root {
                    --primary-color: #2962FF;
                    --background-color: #F8F9FA;
                    --secondary-background-color: #FFFFFF;
                    --text-color: #1A1A1A;
                    --accent-color: #2962FF;
                }
                .stApp {
                    background: linear-gradient(to bottom right, var(--background-color), #E8EAF6);
                }
                /* Card styles */
                div[data-testid="stForm"] {
                    border-radius: 10px;
                    padding: 2rem;
                    background: white;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    border: 1px solid rgba(0, 0, 0, 0.05);
                }
                /* Data display styles */
                div[data-testid="stDataFrame"] {
                    background: white;
                    border-radius: 10px;
                    padding: 1rem;
                    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
                }
                /* Navigation bar styles */
                .nav-container {
                    background: linear-gradient(to right, rgba(41, 98, 255, 0.05), rgba(255, 255, 255, 0));
                    padding: 1rem 2rem;
                    margin: -1rem -1rem 1rem -1rem;
                    position: relative;
                    z-index: 100;
                    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                }
                .nav-links {
                    display: flex;
                    gap: 1.5rem;
                    align-items: center;
                }
                .nav-link {
                    color: var(--text-color);
                    text-decoration: none;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    font-weight: 600;
                    position: relative;
                    letter-spacing: 0.3px;
                    background: rgba(0, 0, 0, 0.03);
                }
                .nav-link:hover {
                    background: rgba(0, 0, 0, 0.05);
                    transform: translateY(-2px);
                }
                .nav-link.active {
                    background: var(--accent-color);
                    color: white;
                }
                /* Theme toggle button */
                .stButton button {
                    background: rgba(0, 0, 0, 0.05);
                    border: none;
                    color: var(--text-color);
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 600;
                }
                .stButton button:hover {
                    background: rgba(0, 0, 0, 0.1);
                    transform: translateY(-2px);
                }
                /* Success message styling */
                div[data-testid="stAlert"] {
                    background: rgba(46, 125, 50, 0.1);
                    border-color: rgba(46, 125, 50, 0.2);
                    color: #2E7D32;
                    border-radius: 8px;
                    padding: 1rem;
                    margin: 1rem 0;
                }
            </style>
        """, unsafe_allow_html=True)

def main():
    # Initialize theme state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Theme toggle in sidebar
    with st.sidebar:
        current_theme = "🌞 Light" if st.session_state.theme == 'light' else "🌙 Dark"
        if st.button(f"Switch to {current_theme} Theme", key='theme_toggle'):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()

    # Apply current theme
    apply_theme(st.session_state.theme)

    # Navigation bar
    st.markdown("""
        <div class="nav-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div class="nav-links">
                    <a href="?page=Portfolio" class="nav-link">📊 Portfolio Dashboard</a>
                    <a href="?page=Analysis" class="nav-link">📈 Technical Analysis</a>
                    <a href="?page=Backtesting" class="nav-link">🔄 Strategy Backtesting</a>
                    <a href="?page=Calculator" class="nav-link">🧮 Degree Calculator</a>
                    <a href="?page=Filter" class="nav-link">🔍 Company Filter</a>
                    <a href="?page=News" class="nav-link">📰 Market News</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Get current page from query params
    query_params = st.query_params
    current_page = query_params.get("page", "Portfolio")

    # Render the appropriate page
    if current_page == "Portfolio":
        from pages.portfolio import render_portfolio_page
        render_portfolio_page()
    elif current_page == "Analysis":
        from pages.analysis import render_analysis_page
        render_analysis_page()
    elif current_page == "Backtesting":
        from pages.backtesting import render_backtesting_page
        render_backtesting_page()
    elif current_page == "Calculator":
        from pages.degree_calculator import render_degree_calculator_page
        render_degree_calculator_page()
    elif current_page == "Filter":
        from pages.company_filter import render_company_filter_page
        render_company_filter_page()
    elif current_page == "News":
        from pages.market_news import render_news_page
        render_news_page()

if __name__ == "__main__":
    main()