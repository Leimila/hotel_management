
import datetime

# Base price for each room type
BASE_PRICES = {
    "Deluxe": 1000,
    "Standard": 3000,
    "Suite": 5000
}

# Seasonal multipliers
SEASONAL_MULTIPLIERS = {
    "Winter": 0.9,  # 10% discount in winter
    "Summer": 1.2,  # 20% increase in summer
    "Spring": 1.0,
    "Fall": 1.0
}

# Demand multipliers (based on day of the week)
DEMAND_MULTIPLIERS = {
    "Monday": 0.9,
    "Tuesday": 0.9,
    "Wednesday": 1.0,
    "Thursday": 1.0,
    "Friday": 1.2,
    "Saturday": 1.5,
    "Sunday": 1.3
}

def get_season(date):
    """Determine the season based on the date."""
    month = date.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def calculate_dynamic_price(room_type, date):
    """
    Calculate the dynamic price for a room based on season, demand, and base price.
    """
    # Get base price for the room type
    base_price = BASE_PRICES.get(room_type, 1000)  # Default to $1000 if room type not found

    # Get seasonal multiplier
    season = get_season(date)
    seasonal_multiplier = SEASONAL_MULTIPLIERS.get(season, 1.0)

    # Get demand multiplier (based on day of the week)
    day_of_week = date.strftime("%A")
    demand_multiplier = DEMAND_MULTIPLIERS.get(day_of_week, 1.0)

    # Calculate final price
    final_price = base_price * seasonal_multiplier * demand_multiplier
    return round(final_price, 2)

# Example usage
if __name__ == "__main__":
    room_type = "Standard"
    date = datetime.date(2023, 12, 25)  # Christmas Day
    price = calculate_dynamic_price(room_type, date)
    print(f"Dynamic price for {room_type} on {date}: ${price}")

    room_type = "Suite"
date = datetime.date(2023, 4, 19)  # April 19, 2023 (Wednesday)
price = calculate_dynamic_price(room_type, date)
print(f"Dynamic price for {room_type} on {date}: ${price}")
