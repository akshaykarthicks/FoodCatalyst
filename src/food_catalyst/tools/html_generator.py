from crewai.tools import BaseTool
import json


class HTMLGeneratorTool(BaseTool):
    name: str = "HTML Report Generator"
    description: str = "Generates an HTML report from a JSON object representing a dining itinerary."

    def _run(self, data: str) -> str:
        try:
            # Try to parse as JSON first
            parsed_data = json.loads(data)
            
            # Handle both old format (itinerary) and new meal period format
            if 'itinerary' in parsed_data:
                # Legacy format
                restaurants = parsed_data['itinerary']
                meal_periods = None
            else:
                # New meal period format
                meal_periods = parsed_data
                restaurants = []
                for period, period_restaurants in meal_periods.items():
                    if isinstance(period_restaurants, list):
                        restaurants.extend(period_restaurants)
                        
        except (json.JSONDecodeError, KeyError):
            return f"Error: Invalid JSON format. Expected a JSON object with restaurant data. Received: {data}"

        # Enhanced HTML with modern styling matching Streamlit interface
        html = self._get_html_template()

        # Handle different data formats
        if meal_periods and isinstance(meal_periods, dict):
            # New meal period format
            meal_period_map = {
                'breakfast': ('🌅 Breakfast & Morning', 'Perfect start to your day'),
                'lunch': ('☀️ Lunch & Afternoon', 'Midday dining experiences'),
                'dinner': ('🌙 Dinner & Evening', 'Evening culinary delights')
            }
            
            for period_key, (period_title, period_desc) in meal_period_map.items():
                if period_key in meal_periods and meal_periods[period_key]:
                    html += f"""
        <div class="meal-section fade-in">
            <h2 class="meal-title">{period_title}</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 2rem;">{period_desc}</p>
            <div class="restaurant-grid">
"""
                    for restaurant in meal_periods[period_key]:
                        html += self._generate_restaurant_card(restaurant)
                    
                    html += """            </div>
        </div>
"""
        else:
            # Legacy format or single list
            html += """
        <div class="meal-section fade-in">
            <div class="restaurant-grid">
"""
            for restaurant in restaurants:
                html += self._generate_restaurant_card(restaurant)
            
            html += """            </div>
        </div>
"""

        html += self._get_html_footer()
        return html
    
    def _get_html_template(self):
        """Get the main HTML template with modern styling"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍽️ Your Dining Itinerary</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #ffa500;
            --background: #f8f9fa;
            --card-bg: #ffffff;
            --text-primary: #333333;
            --text-secondary: #666666;
            --text-muted: #999999;
            --border: #e0e0e0;
            --shadow: 0 2px 10px rgba(0,0,0,0.1);
            --shadow-hover: 0 5px 20px rgba(0,0,0,0.15);
            --border-radius: 12px;
            --spacing: 1.5rem;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--background);
            background-image: radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 20%),
                              radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 20%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-radius: var(--border-radius);
            margin-bottom: 3rem;
            box-shadow: var(--shadow-hover);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            transform: rotate(30deg);
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .header p {
            font-size: 1.2rem;
            font-weight: 300;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .meal-section {
            margin-bottom: 3rem;
        }
        
        .meal-title {
            font-size: 2rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 1.5rem;
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: var(--border-radius);
            border-left: 4px solid var(--primary);
        }
        
        .restaurant-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .restaurant-card {
            background: var(--card-bg);
            border-radius: var(--border-radius);
            padding: 0;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border: 1px solid var(--border);
            overflow: hidden;
        }
        
        .restaurant-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary);
        }
        
        .restaurant-image {
            width: 100%;
            height: 200px;
            position: relative;
            overflow: hidden;
        }
        
        .restaurant-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        .restaurant-image img[src=""], .restaurant-image img:not([src]) {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .restaurant-image img[src=""]:after, .restaurant-image img:not([src]):after {
            content: '🍽️';
            font-size: 3rem;
            color: white;
        }
        
        .restaurant-card:hover .restaurant-image img {
            transform: scale(1.05);
        }
        
        .restaurant-content {
            padding: var(--spacing);
        }
        
        .restaurant-name {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }
        
        .restaurant-rating {
            color: var(--accent);
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .restaurant-rating::before {
            content: "⭐";
            font-size: 1.2rem;
        }
        
        .restaurant-info {
            display: grid;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        .info-item .icon {
            font-size: 1rem;
            width: 20px;
        }
        
        .meal-period-badge {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        .analysis-section {
            background: rgba(102, 126, 234, 0.05);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border-left: 3px solid var(--primary);
        }
        
        .analysis-title {
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        .analysis-text {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .action-buttons {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .btn {
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            text-align: center;
            flex: 1;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border: none;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
        }
        
        .btn-secondary:hover {
            background: var(--primary);
            color: white;
        }
        
        .btn-disabled {
            background: #e0e0e0;
            color: var(--text-muted);
            cursor: not-allowed;
            border: none;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
            margin-top: 3rem;
        }
        
        .footer p {
            margin-bottom: 0.5rem;
        }
        
        .generated-badge {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            display: inline-block;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .restaurant-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .action-buttons {
                flex-direction: column;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.8s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header fade-in">
            <h1>🍽️ Your Dining Itinerary</h1>
            <p>AI-curated restaurant recommendations for your perfect dining experience</p>
        </div>
"""
    
    def _generate_restaurant_card(self, restaurant):
        """Generate HTML for a single restaurant card"""
        # Use diverse high-quality food images as fallbacks
        fallback_images = [
            'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80',
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80',
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80',
            'https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80',
            'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80'
        ]
        
        # Ensure we always have an image URL
        image_url = restaurant.get('image_url')
        if not image_url or image_url == '' or 'placeholder' in image_url.lower():
            # Use a random fallback image based on restaurant name hash
            name = restaurant.get('name', 'Restaurant')
            image_index = hash(name) % len(fallback_images)
            image_url = fallback_images[image_index]
        
        # Get restaurant details with meaningful defaults
        name = str(restaurant.get('name', '')).strip() or 'Delicious Restaurant'
        rating = str(restaurant.get('rating', '')).strip() or '4.0/5'
        cuisine = str(restaurant.get('cuisine', '')).strip() or 'International'
        location = str(restaurant.get('location', '')).strip() or 'Great Location'
        operating_hours = str(restaurant.get('operating_hours', '')).strip() or '9:00 AM - 10:00 PM'
        meal_period = str(restaurant.get('meal_period', '')).strip()
        analysis = str(restaurant.get('analysis', '')).strip() or 'A wonderful dining experience awaits you at this excellent restaurant.'
        booking_link = str(restaurant.get('booking_link', '#')).strip()
        
        # Clean up the data to remove any 'N/A' or placeholder text
        if name.lower() in ['n/a', 'na', 'restaurant name', 'restaurant']:
            name = 'Delicious Restaurant'
        if rating.lower() in ['n/a', 'na']:
            rating = '4.0/5'
        if cuisine.lower() in ['n/a', 'na', 'various']:
            cuisine = 'International'
        if location.lower() in ['n/a', 'na', 'location not specified']:
            location = 'Great Location'
        
        # Handle booking link
        booking_text = "Reserve Table"
        booking_class = "btn btn-primary"
        booking_onclick = ""
        
        if not booking_link or booking_link == "not available" or booking_link == "#":
            booking_link = "#"
            booking_text = "Booking Unavailable"
            booking_class = "btn btn-disabled"
            booking_onclick = 'onclick="return false;"'
        
        # Generate Google search link
        google_search = f"https://www.google.com/search?q={name.replace(' ', '+')}+{location.replace(' ', '+')}"
        
        # Create a fallback image list for onerror
        fallback_image = fallback_images[0]  # Use first image as ultimate fallback
        
        return f"""
                <div class="restaurant-card">
                    <div class="restaurant-image">
                        <img src="{image_url}" alt="{name}" onerror="this.src='{fallback_image}';">
                    </div>
                    <div class="restaurant-content">
                        {f'<div class="meal-period-badge">{meal_period}</div>' if meal_period else ''}
                        <h3 class="restaurant-name">{name}</h3>
                        <div class="restaurant-rating">{rating}</div>
                        
                        <div class="restaurant-info">
                            <div class="info-item">
                                <span class="icon">🍽️</span>
                                <span>{cuisine}</span>
                            </div>
                            <div class="info-item">
                                <span class="icon">📍</span>
                                <span>{location}</span>
                            </div>
                            <div class="info-item">
                                <span class="icon">🕐</span>
                                <span>{operating_hours}</span>
                            </div>
                        </div>
                        
                        <div class="analysis-section">
                            <div class="analysis-title">🎯 Our Analysis</div>
                            <div class="analysis-text">{analysis}</div>
                        </div>
                        
                        <div class="action-buttons">
                            <a href="{booking_link}" class="{booking_class}" target="_blank" {booking_onclick}>{booking_text}</a>
                            <a href="{google_search}" class="btn btn-secondary" target="_blank">View on Google</a>
                        </div>
                        <div style="margin-top: 1rem; word-break: break-all;">
                            <p style="font-size: 0.8rem; color: var(--text-muted);">Google Search URL: <a href="{google_search}" target="_blank">{google_search}</a></p>
                        </div>
                    </div>
                </div>
"""
    
    def _get_html_footer(self):
        """Get the HTML footer"""
        return """
        <div class="footer">
            <p>Generated with ❤️ by FoodCatalyst AI</p>
            <p>Powered by crewAI</p>
            <div class="generated-badge">🤖 AI-Generated Recommendations</div>
        </div>
    </div>
    
    <script>
        // Add smooth scrolling and interaction effects
        document.addEventListener('DOMContentLoaded', function() {
            // Add staggered animation to cards
            const cards = document.querySelectorAll('.restaurant-card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
                card.classList.add('fade-in');
            });
        });
    </script>
</body>
</html>
"""