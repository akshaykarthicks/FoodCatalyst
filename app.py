# SQLite workaround for cloud environments
try:
    __import__('pysqlite3')
    import sys as _sys
    _sys.modules['sqlite3'] = _sys.modules.pop('pysqlite3')
except ImportError:
    pass




import streamlit as st
import os
import sys
import json
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path so we can import the FoodCatalyst crew
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Set page configuration
st.set_page_config(
    page_title="FoodCatalyst - AI Dining Assistant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# Custom CSS for FoodCatalyst
st.markdown("""
<style>
    .food-catalyst-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .food-catalyst-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .food-catalyst-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .stButton>button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .result-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .restaurant-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .restaurant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .restaurant-name {
        color: #667eea;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .restaurant-rating {
        color: #ffa500;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="food-catalyst-header">
    <h1>🍽️ FoodCatalyst</h1>
    <p>AI-Powered Restaurant Discovery & Planning</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
Welcome to FoodCatalyst, your AI-powered dining assistant! Our system uses multiple AI agents to research, analyze, and create personalized dining itineraries based on your preferences.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("🍽️ Your Preferences")
    
    topic = st.text_input("Cuisine/Food Type", "Indian", help="e.g., Italian, Sushi, Vegan")
    location = st.text_input("Location", "Chennai", help="e.g., New York, Paris, Tokyo")
    date_option = st.selectbox("When to Dine?", ["Today", "Tomorrow", "This Weekend", "Next Week"])
    
    with st.expander("⚙️ Advanced Settings", expanded=False):
        current_year = st.number_input("Current Year", value=datetime.now().year, min_value=2020, max_value=2030)

    st.markdown("---")
    
    with st.expander("🔍 How It Works", expanded=True):
        st.markdown("""
        - **Scout Agent**: Discovers top-rated and trending restaurants.
        - **Critic Agent**: Analyzes reviews, menus, and customer feedback.
        - **Planner Agent**: Creates a personalized dining itinerary for you.
        """)

    with st.expander("💡 Tips", expanded=False):
        st.markdown("""
        - Be specific with your cuisine preferences.
        - Try different locations to discover new places.
        - Check back for updated recommendations.
        """)

    with st.expander("🌟 Featured Cuisines", expanded=False):
        st.markdown("- Italian\n- Japanese\n- Mexican\n- Indian\n- French\n- Thai\n- Mediterranean")

    with st.expander("📍 Popular Cities", expanded=False):
        st.markdown("- New York\n- London\n- Paris\n- Tokyo\n- Bangkok\n- Rome\n- Barcelona")

# Main content area
st.subheader("🤖 Your Personal Dining Assistant")

# Create input form
with st.form("food_preferences_main"):
    st.markdown("##### Tell us what you're craving!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        topic_input = st.text_input("Cuisine or food type", value=topic)
    with col2:
        location_input = st.text_input("City or location", value=location)
    with col3:
        date_input = st.selectbox("When", ["Today", "Tomorrow", "This Weekend", "Next Week"], index=["Today", "Tomorrow", "This Weekend", "Next Week"].index(date_option))
    
    submitted = st.form_submit_button("🍽️ Discover Restaurants")

# Process the form submission
if submitted:
    if topic_input and location_input:
        st.info("🔍 Our AI agents are searching for the best restaurants...")

        try:
            from food_catalyst.crew import FoodCatalyst

            inputs = {
                'topic': topic_input,
                'location': location_input,
                'current_year': str(current_year)
            }

            result = FoodCatalyst().crew().kickoff(inputs=inputs)

            st.success("✅ Discovery complete! Here are your personalized recommendations:")

            st.markdown("### 📋 Your Dining Itinerary")

            json_match = re.search(r'\{.*\}', result.raw, re.DOTALL)
            if json_match:
                try:
                    itinerary_data = json.loads(json_match.group())
                    if 'itinerary' in itinerary_data:
                        for i, restaurant in enumerate(itinerary_data['itinerary'], 1):
                            st.markdown(f"""
                            <div class="restaurant-card">
                                <div class="restaurant-name">#{i} {restaurant.get('name', 'N/A')}</div>
                                <div class="restaurant-rating">⭐ {restaurant.get('rating', 'N/A')}</div>
                                <div class="restaurant-cuisine">🍽️ {restaurant.get('cuisine', 'N/A')}</div>
                                <div class="restaurant-location">📍 {restaurant.get('location', 'N/A')}</div>
                                <div class="restaurant-analysis">
                                    <h4>Analysis:</h4>
                                    <p>{restaurant.get('analysis', 'No analysis available.')}</p>
                                </div>
                                <a href="https://www.google.com/search?q={restaurant.get('name', '').replace(' ', '+')}+{restaurant.get('location', '').replace(' ', '+')}" target="_blank" class="stButton">
                                    <button>Google Search</button>
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("Could not find an itinerary in the result. The AI agents might be having trouble.")
                except json.JSONDecodeError:
                    st.error("The Result  might be incorrect.Kindly check twice !!")
            else:
                st.warning("No structured data found in the result. The AI agents might not have found any restaurants.")

            if os.path.exists("report.html"):
                st.markdown("### 📄 HTML Report Preview")
                with open("report.html", "r", encoding="utf-8") as f:
                    html_content = f.read()
                    st.components.v1.html(html_content, height=600, scrolling=True)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your API keys and configuration in the .env file.")
    else:
        st.warning("Please fill in both cuisine type and location.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Powered by <strong>crewAI</strong> | Made with ❤️ for food lovers</p>
</div>
""", unsafe_allow_html=True)
