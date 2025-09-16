# Meal Planning Feature

## Overview
Added time-based meal planning to FoodCatalyst that organizes restaurant recommendations by meal periods:
- **Breakfast/Morning** (7AM-11AM): cafes, breakfast spots, brunch places
- **Lunch/Afternoon** (11AM-4PM): lunch restaurants, casual dining
- **Dinner/Evening** (5PM-10PM): dinner restaurants, fine dining

## Implementation Details

### UI Changes (app.py)
- Added meal period multiselect in sidebar and main form
- Enhanced restaurant cards to show operating hours and meal period suitability
- Results now grouped by meal periods with appropriate emojis
- Updated help text and tips

### Agent Configuration (agents.yaml)
- Scout agent now focuses on meal-appropriate restaurants
- Critic agent analyzes meal-specific aspects (breakfast quality, lunch portions, dinner ambiance)
- Planner agent organizes by meal periods and considers operating hours

### Task Configuration (tasks.yaml)
- Research task seeks 3-5 restaurants per meal period
- Analysis task considers meal-specific factors
- Planning task outputs JSON with meal period keys (breakfast, lunch, dinner)
- Updated restaurant schema to include meal_period and operating_hours

### Key Features
- Time-aware restaurant discovery
- Meal period appropriate recommendations
- Operating hours consideration
- Enhanced visual organization of results
- Backward compatibility with old itinerary format

## Usage
Users can now select multiple meal periods and get organized recommendations for each time of day, making it easier to plan full-day dining experiences.