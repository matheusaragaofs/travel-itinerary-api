from flask import Blueprint, jsonify
from services.travel_route import criar_rota_viagem
from templates.prompt_template import prompt_template
from models.llm_models import get_model

home_route = Blueprint('home_route', __name__)

@home_route.route('/', methods=['GET'])
def home():
    # Modelo
    llm = get_model("openai")

    # Dados de entrada
    destinos_interesse = "Rio de Janeiro"
    recomendacao_hospedagem = "Hotel"
    data_inicio = "04 de julho a 06 de julho"
    preferencias_atividades = "Museus, gastronomia local, passeios a pé"
    orcamento_disponivel = "até 5 mil reais"
    necessidades_especiais = "Sem necessidade especial"

    # Chamada da função
    json_rota = criar_rota_viagem(llm, prompt_template, destinos_interesse, recomendacao_hospedagem, data_inicio, preferencias_atividades, orcamento_disponivel, necessidades_especiais)

    response_data = {
        **json_rota,
        "status": "success"
    }
    return jsonify(response_data)
