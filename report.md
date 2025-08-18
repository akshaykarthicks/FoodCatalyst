```html
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
    }
    .restaurant-image img {
        width: 100%;
        height: auto;
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
</style>
</head>
<body>
<div class="container">
    <h1>Your Dining Itinerary</h1>

    <div class="restaurant">
        <div class="restaurant-image">
            <img src="https://b.zmtcdn.com/data/pictures/7/66997/c188f8eba89d505d143653653a3edce1_featured_v2.jpg?fit=around|771.75:416.25&crop=771.75:416.25;*,*)" alt="Ottimo Cucina Italiana">
        </div>
        <div class="restaurant-details">
            <h2>Ottimo Cucina Italiana</h2>
            <p><strong>Cuisine:</strong> Italian</p>
            <p><strong>Location:</strong> ITC Grand Chola, Guindy, Chennai</p>
            <p class="rating"><strong>Rating:</strong> 4.6</p>
            <h3>Analysis</h3>
            <p>Consistently high ratings, likely offers a wide variety of classic Italian dishes. Price point is high (approx. ₹6500 for two).</p>
            <a href="https://www.zomato.com/chennai/ottimo-cucina-italiana-itc-grand-chola-guindy" class="booking-link" target="_blank">Book Now</a>
        </div>
    </div>
    
    <div class="restaurant">
        <div class="restaurant-image">
            <img src="https://b.zmtcdn.com/data/pictures/4/65624/4d5290701b2d5d36fcb976a5d39a3ea8.jpg?fit=around|771.75:416.25&crop=771.75:416.25;*,*" alt="Tuscana Pizzeria">
        </div>
        <div class="restaurant-details">
            <h2>Tuscana Pizzeria</h2>
            <p><strong>Cuisine:</strong> Italian (Pizza)</p>
            <p><strong>Location:</strong> Multiple locations in Chennai (Nungambakkam, Alwarpet, ECR)</p>
            <p class="rating"><strong>Rating:</strong> 4.3</p>
            <h3>Analysis</h3>
            <p>Highly rated, specializes in pizza.  Offers thin crust wood-fired pizzas with various bases. Price point is moderate (approx. ₹1200-₹1600 for two).</p>
            <a href="https://www.zomato.com/chennai/tuscana-pizzeria-nungambakkam" class="booking-link" target="_blank">Book Now</a>
        </div>
    </div>
    
    <div class="restaurant">
        <div class="restaurant-image">
            <img src="https://b.zmtcdn.com/data/pictures/chains/2/68502/ba1d66950aeaab3fcbdd296f5fab5b83.jpeg" alt="Little Italy">
        </div>
        <div class="restaurant-details">
            <h2>Little Italy</h2>
            <p><strong>Cuisine:</strong> Vegetarian Italian</p>
            <p><strong>Location:</strong> Multiple locations in Chennai (Besant Nagar, Nungambakkam)</p>
            <p class="rating"><strong>Rating:</strong> 4.5</p>
            <h3>Analysis</h3>
            <p>Good choice for vegetarian Italian food. Price point is moderate (approx. ₹1100-₹1300 for two).</p>
            <a href="https://www.zomato.com/chennai/little-italy-besant-nagar" class="booking-link" target="_blank">Book Now</a>
        </div>
    </div>
    
</div>
</body>
</html>
```