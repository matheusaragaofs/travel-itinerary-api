from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=[
        "destination",
        "travel_period",
        "preffered_travel_styles",
        "budget",
        "expected_json_schema",
    ],
    template=(
        """
        You will be a travel expert, your role is to create travel itineraries based on some information that will be provided below
        Choose the most popular and famous activities in that location
        Please create a detailed travel itinerary with the following information:

        The destination of interest is: {destination};
        The travel period is 7 days, here is the period: {travel_period};
        The travel budget for the 7 days of the trip is: {budget};
        
        Generate a travel plan in the following JSON format: {expected_json_schema}
            
        Make sure there are 3 accommodation recommendations in: "recommended_accommodations";
        Make sure there are 3 restaurants recommendations in: "recommended_restaurants";
        Make sure there are 3 extra activities based on preffered travel styles in: "extra_activities_based_on_preffered_travel_styles"
        based on the preffered travel styles: {preffered_travel_styles};
        Make sure activities at close times are relatively close together;
        Make sure to fill in all required fields with appropriate data.
        Make sure if the address has "R. " in it, it is replaced with "Rua " and if it has "Av. " in it, it is replaced with "Avenida ", and it doesnt need
        the zipcode in the address and the format should be "street_name, number, neighborhood, city - state".

    """
    ),
)
