from dotenv import load_dotenv
from flask import Flask, request, jsonify
from services.travel_route import criar_rota_viagem
from templates.prompt_template import prompt_template
from models.llm_models import get_model

app = Flask(__name__)
load_dotenv()


@app.route("/create-itinerary", methods=["POST"])
def home():
    llm = get_model("openai")

    data = request.json

    destinos_interesse = data.get("destinos_interesse")
    recomendacao_hospedagem = data.get("recomendacao_hospedagem")
    data_inicio = data.get("data_inicio")
    preferencias_atividades = data.get("preferencias_atividades")
    orcamento_disponivel = data.get("orcamento_disponivel")
    necessidades_especiais = data.get("necessidades_especiais")

    try:
        json_rota = criar_rota_viagem(
            llm,
            prompt_template,
            destinos_interesse,
            recomendacao_hospedagem,
            data_inicio,
            preferencias_atividades,
            orcamento_disponivel,
            necessidades_especiais,
        )
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": "Invalid response from criar_rota_viagem",
                "error": str(e),
            }
        )

    response_data = {**json_rota, "status": "success"}
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
