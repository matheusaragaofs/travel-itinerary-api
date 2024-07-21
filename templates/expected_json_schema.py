day_template = """
{
    "date_day": "string",
    "morning": {
        "activity": "string",
        "location": "string",
        "latitude": "string",
        "longitude": "string",
        "time": "string",
        "cost": "string"
    },
    "afternoon": {
        "activity": "string",
        "location": "string",
        "latitude": "string",
        "longitude": "string",
        "time": "string",
        "cost": "string"
    },
    "night": {
        "activity": "string",
        "location": "string",
        "latitude": "string",
        "longitude": "string",
        "time": "string",
        "cost": "string"
    }
}
"""


expected_json_schema = f"""
{{
    "destination": "string",
    "travel_period": "string",
    "preferred_travel_style": "string",
    "budget": "string", 
    "local_currency_symbol": "string",
    "local_currency": "string",
    
    "itinerary": {{
        "sunday": {day_template}
        "monday": {day_template},
        "tuesday": {day_template},
        "wednesday": {day_template},
        "thursday": {day_template},
        "friday": {day_template},
        "saturday": {day_template},
    }},
    "recommended_accommodations": [
        {{
            "name": "string",
            "location": "string",
            "latitude": "string",
            "longitude": "string",
            "average_price": "string",
        }}
    ],
    "recommended_restaurants": [
        {{
            "name": "string",
            "location": "string",
            "latitude": "string",
            "longitude": "string",
            "average_price": "string",
            "restaurant_type": "string"
        }}
    ],
    "extra_activities_based_on_preffered_travel_styles": [
        {{
            "name": "string",
            "description": "string",
            "cost": "string"
        }}
    ]
   
}}
"""
