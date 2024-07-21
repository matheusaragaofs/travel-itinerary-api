itinerary = {
    "friday": {
        "afternoon": {
            "activity": "Explore the Texas Tech University Campus",
            "average_price": "Free",
            "latitude": "33.5843",
            "location": "2500 Broadway, Lubbock, TX",
            "longitude": "-101.8783",
            "time": "12:00 PM - 2:00 PM",
        },
        "date_day": "2024-07-26",
        "morning": {
            "activity": "Visit Bayer Museum of Agriculture",
            "average_price": "$5",
            "latitude": "33.5952",
            "location": "1121 Canyon Lake Dr, Lubbock, TX",
            "longitude": "-101.8515",
            "time": "9:00 AM - 11:00 AM",
        },
        "night": {
            "activity": "Dance at Charley B's",
            "average_price": "$10",
            "latitude": "33.5916",
            "location": "5402 4th St, Lubbock, TX",
            "longitude": "-101.9337",
            "time": "9:00 PM - 12:00 AM",
        },
    },
    "monday": {
        "afternoon": {
            "activity": "Walk through Lubbock Memorial Arboretum",
            "average_price": "Free",
            "latitude": "33.5700",
            "location": "4111 University Ave, Lubbock, TX",
            "longitude": "-101.8748",
            "time": "1:00 PM - 3:00 PM",
        },
        "date_day": "2024-07-22",
        "morning": {
            "activity": "Visit the National Ranching Heritage Center",
            "average_price": "Free",
            "latitude": "33.5903",
            "location": "3121 4th St, Lubbock, TX",
            "longitude": "-101.8830",
            "time": "9:00 AM - 12:00 PM",
        },
    },
}

extra_activities_based_on_preferred_travel_styles = [
    {
        "activity": "Nightclub at Club Luxor",
        "average_price": "$20",
        "latitude": "33.5832",
        "location": "2211 Marsha Sharp Fwy, Lubbock, TX",
        "longitude": "-101.8651",
        "time": "10:00 PM - 2:00 AM",
    },
    {
        "activity": "Hiking at Lubbock Lake Landmark",
        "average_price": "Free",
        "latitude": "33.6311",
        "location": "2401 Landmark Dr, Lubbock, TX",
        "longitude": "-101.8927",
        "time": "9:00 AM - 12:00 PM",
    },
    {
        "activity": "Attend Lubbock Arts Festival",
        "average_price": "$10",
        "latitude": "33.5904",
        "location": "Lubbock Memorial Civic Center",
        "longitude": "-101.8478",
        "time": "10:00 AM - 6:00 PM",
    },
]

accommodations = [
    {
        "average_price": "$120/night",
        "latitude": "33.5908",
        "location": "2322 Mac Davis Ln, Lubbock, TX",
        "longitude": "-101.8726",
        "name": "Overton Hotel & Conference Center",
        "type": "Hotel",
    },
    {
        "average_price": "$110/night",
        "latitude": "33.5907",
        "location": "2309 Mac Davis Ln, Lubbock, TX",
        "longitude": "-101.8724",
        "name": "Hyatt Place Lubbock",
        "type": "Hotel",
    },
]

restaurants = [
    {
        "average_price": "$15",
        "latitude": "33.5816",
        "location": "620 19th St, Lubbock, TX",
        "longitude": "-101.8485",
        "name": "Cast Iron Grill",
        "type": "American",
    },
    {
        "average_price": "$25",
        "latitude": "33.5843",
        "location": "901 17th St, Lubbock, TX",
        "longitude": "-101.8479",
        "name": "La Diosa Cellars",
        "type": "Spanish",
    },
    {
        "average_price": "$20",
        "latitude": "33.5807",
        "location": "2605 19th St, Lubbock, TX",
        "longitude": "-101.8723",
        "name": "Café J",
        "type": "American",
    },
]

mocked_response = {
    "itinerary": itinerary,
    "recommended_accommodations": accommodations,
    "recommended_restaurants": restaurants,
    "extra_activities_based_on_preferred_travel_styles": extra_activities_based_on_preferred_travel_styles,
}
