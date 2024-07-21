activity_template = """
    {
        "activity": "string",
        "address": "string",
        "latitude": "string",
        "longitude": "string",
        "time": "string",
        "average_cost": "string"
    }
"""

recomendation_template = """
    {
        "name": "string",
        "address": "string",
        "latitude": "string",
        "longitude": "string",
        "average_cost": "string",
        "type": "string"
    }
"""


day_template = f"""
    {{
        "date_day": "string",
        "morning": {activity_template},
        "afternoon": {activity_template},
        "night": {activity_template}
    }}
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
    "recommended_accommodations": [ {recomendation_template} ],
    "recommended_restaurants": [ {recomendation_template} ],
    "extra_activities_based_on_preffered_travel_styles": [ {activity_template} ]
   
}}
"""
