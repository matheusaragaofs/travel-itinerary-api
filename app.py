from dotenv import load_dotenv
from flask import Flask, request, jsonify
from services.travel_route import generate_itinerary
from templates.prompt_template import prompt_template
from models.llm_models import get_model

app = Flask(__name__)
load_dotenv()


@app.route("/generate-itinerary", methods=["POST"])
def home():
    llm = get_model("openai")

    data = request.json

    destination = data.get("destination")
    travel_period = data.get("travel_period")
    preffered_travel_styles = data.get("preffered_travel_styles")
    budget = data.get("budget")

    try:
        response = generate_itinerary(
            llm,
            prompt_template,
            destination,
            travel_period,
            preffered_travel_styles,
            budget,
        )

    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": "Invalid response from generate_itinerary",
                "error": str(e),
            }
        )

    return response


if __name__ == "__main__":
    app.run(debug=True)
