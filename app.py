# SQLite workaround for Streamlit Cloud (Linux environment)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # On Windows or if pysqlite3 is not available, use system sqlite3
    pass

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Pro App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Hero Section
with st.container():
    st.markdown("""
        <div class='hero-section'>
            <h1>Pro App</h1>
            <h2>The modern way to build data applications.</h2>
            <p class='subtitle'>Visually stunning, highly functional, and production-grade. Create interfaces that users love.</p>
            <a href='#' class='cta-button'>Get Started Now</a>
        </div>
    """, unsafe_allow_html=True)

# --- Features Section ---
with st.container():
    st.markdown("""
        <div class='features-section'>
            <h2>Why Pro App is Different</h2>
            <div class='features-grid'>
                <div class='feature-card'>
                    <h3>🚀</h3>
                    <h4>Blazing Fast</h4>
                    <p>Optimized for performance, ensuring a smooth and responsive user experience.</p>
                </div>
                <div class='feature-card'>
                    <h3>🎨</h3>
                    <h4>Beautifully Designed</h4>
                    <p>Modern aesthetics and a clean interface that users will love at first sight.</p>
                </div>
                <div class='feature-card'>
                    <h3>💡</h3>
                    <h4>Highly Intuitive</h4>
                    <p>Designed with user experience in mind, making it easy to use and navigate.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
