#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv


from food_catalyst.crew import FoodCatalyst

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.

    """
    load_dotenv()
    inputs = {
        'topic': 'Biryani',
        'location': 'Chennai',
        'current_year': str(datetime.now().year)
    }
    
    result = FoodCatalyst().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")


if __name__ == "__main__":
    run()