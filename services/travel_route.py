import json
from langchain.chains import LLMChain
from templates.expected_json_schema import expected_json_schema


class InvalidResponseError(Exception):
    pass


def generate_itinerary(
    llm,
    prompt_template,
    destination,
    travel_period,
    preffered_travel_styles,
    budget,
):
    while True:
        chain = LLMChain(llm=llm, prompt=prompt_template)
        travel_data = {
            "destination": destination,
            "travel_period": travel_period,
            "preffered_travel_styles": preffered_travel_styles,
            "budget": budget,
            "expected_json_schema": expected_json_schema,
        }
        response = chain.run(travel_data)
        cleaned_string = response.replace("```json", "").replace("```", "")

        parsed_json = json.loads(cleaned_string)
        return parsed_json
