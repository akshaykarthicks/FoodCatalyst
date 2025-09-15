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
    st.markdown("---")
    
    topic = st.text_input("What type of cuisine are you interested in?", "Biryani")
    location = st.text_input("Where would you like to dine?", "Chennai")
    
    st.markdown("---")
    st.subheader("🔍 How it works")
    st.markdown("""
    1. **Scout Agent** discovers trending restaurants
    2. **Critic Agent** analyzes reviews and menus
    3. **Planner Agent** creates your personalized itinerary
    """)
    
    st.markdown("---")
    st.subheader("⚙️ Advanced Settings")
    current_year = st.number_input("Current Year", value=datetime.now().year, min_value=2020, max_value=2030)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Enter your dining preferences")
    
    # Create input form
    with st.form("food_preferences"):
        st.markdown("#### 🍽️ What would you like to eat?")
        topic_input = st.text_input("Cuisine or food type", value=topic, placeholder="e.g., Italian, Sushi, Vegan")
        
        st.markdown("#### 📍 Where would you like to dine?")
        location_input = st.text_input("City or location", value=location, placeholder="e.g., New York, Paris, Tokyo")
        
        st.markdown("#### 📅 When are you planning to dine?")
        date_option = st.selectbox("When", ["Today", "Tomorrow", "This Weekend", "Next Week"])
        
        submitted = st.form_submit_button("🍽️ Discover Restaurants")
    
    # Process the form submission
    if submitted:
        if topic_input and location_input:
            st.info("🔍 Our AI agents are searching for the best restaurants...")
            
            try:
                # Import and run the FoodCatalyst crew
                from food_catalyst.crew import FoodCatalyst
                
                # Prepare inputs
                inputs = {
                    'topic': topic_input,
                    'location': location_input,
                    'current_year': str(current_year)
                }
                
                # Run the crew
                result = FoodCatalyst().crew().kickoff(inputs=inputs)
                
                # Display results
                st.success("✅ Discovery complete! Here are your personalized recommendations:")
                
                # Try to parse the result and display in a nice format
                st.markdown("### 📋 Your Dining Itinerary")
                
                # Try to extract JSON from the result
                json_match = re.search(r'\{.*\}', result.raw, re.DOTALL)
                if json_match:
                    try:
                        itinerary_data = json.loads(json_match.group())
                        if 'itinerary' in itinerary_data:
                            # Display restaurant cards
                            for i, restaurant in enumerate(itinerary_data['itinerary'], 1):
                                with st.container():
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
                                        <a href="{restaurant.get('booking_link', '#')}" target="_blank" class="stButton">
                                            <button>Book Now</button>
                                        </a>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.text_area("Raw Results", result.raw, height=300)
                    except json.JSONDecodeError:
                        st.text_area("Raw Results", result.raw, height=300)
                else:
                    st.text_area("Raw Results", result.raw, height=300)
                
                # Also show the HTML report if it was generated
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

with col2:
    st.subheader("💡 Tips")
    st.markdown("""
    - Be specific with your cuisine preferences
    - Try different locations to discover new places
    - Check back regularly for updated recommendations
    """)
    
    st.markdown("---")
    st.subheader("🌟 Featured Cuisines")
    st.markdown("""
    - Italian
    - Japanese
    - Mexican
    - Indian
    - French
    - Thai
    - Mediterranean
    """)
    
    st.markdown("---")
    st.subheader("📍 Popular Cities")
    st.markdown("""
    - New York
    - London
    - Paris
    - Tokyo
    - Bangkok
    - Rome
    - Barcelona
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Powered by <strong>crewAI</strong> | Made with ❤️ for food lovers</p>
</div>
""", unsafe_allow_html=True)