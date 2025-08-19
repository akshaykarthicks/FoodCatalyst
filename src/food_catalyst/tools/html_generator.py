from crewai.tools import BaseTool
import json


class HTMLGeneratorTool(BaseTool):
    name: str = "HTML Report Generator"
    description: str = "Generates an HTML report from a JSON object representing a dining itinerary."

    def _run(self, data: str) -> str:
        try:
            # Try to parse as JSON first
            parsed_data = json.loads(data)
            # Check if it's the itinerary format or full result
            if 'itinerary' in parsed_data:
                itinerary = parsed_data['itinerary']
            else:
                # If not, try to find itinerary in nested structure
                itinerary = parsed_data
        except (json.JSONDecodeError, KeyError):
            return f"Error: Invalid JSON format. Expected a JSON object with an 'itinerary' key. Received: {data}"

        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Your Dining Itinerary</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
            body {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f7f6;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                text-align: center;
                color: #2c3e50;
                margin-bottom: 40px;
            }
            .restaurant {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                display: flex;
                gap: 20px;
            }
            .restaurant-image {
                flex: 1;
                min-width: 200px;
            }
            .restaurant-image img {
                width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 8px;
            }
            .restaurant-details {
                flex: 2;
            }
            .restaurant h2 {
                margin-top: 0;
                color: #e74c3c;
            }
            .rating {
                font-weight: bold;
                color: #f39c12;
                font-size: 1.1em;
            }
            .booking-link {
                display: inline-block;
                margin-top: 15px;
                padding: 10px 15px;
                background-color: #3498db;
                color: #ffffff;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s;
            }
            .booking-link:hover {
                background-color: #2980b9;
            }
            .booking-link.disabled {
                background-color: #bdc3c7;
                cursor: not-allowed;
            }
            .booking-link.disabled:hover {
                background-color: #bdc3c7;
            }
        </style>
        </head>
        <body>
        <div class="container">
            <h1>Your Dining Itinerary</h1>
        """

        for restaurant in itinerary:
            # Ensure we always have an image URL
            image_url = restaurant.get('image_url')
            if not image_url or image_url == '' or 'placeholder' in image_url.lower():
                # Use a generic food image
                image_url = 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&h=400&q=80'
            
            # Handle booking link
            booking_link = restaurant.get('booking_link', '#')
            booking_text = "Book Now"
            booking_class = "booking-link"
            
            # If no booking link is available, disable the button
            if not booking_link or booking_link == "not available" or booking_link == "#":
                booking_link = "#"
                booking_text = "Booking Unavailable"
                booking_class += " disabled"
            
            html += f"""
            <div class="restaurant">
                <div class="restaurant-image">
                    <img src="{image_url}" alt="{restaurant.get('name', 'Restaurant')}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&h=400&q=80';">
                </div>
                <div class="restaurant-details">
                    <h2>{restaurant.get('name', 'N/A')}</h2>
                    <p><strong>Cuisine:</strong> {restaurant.get('cuisine', 'N/A')}</p>
                    <p><strong>Location:</strong> {restaurant.get('location', 'N/A')}</p>
                    <p class="rating"><strong>Rating:</strong> {restaurant.get('rating', 'N/A')}</p>
                    <h3>Analysis</h3>
                    <p>{restaurant.get('analysis', 'N/A')}</p>
                    <a href="{booking_link}" class="{booking_class}" target="_blank" {'onclick="return false;"' if 'disabled' in booking_class else ''}>{booking_text}</a>
                </div>
            </div>
            """

        html += """
        </div>
        </body>
        </html>
        """
        return html