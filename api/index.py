from flask import Flask
from dotenv import load_dotenv
import os
import os
import json
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)
load_dotenv() 
@app.route('/', methods=['GET'])

def home():
    OPEN_API_KEY = os.environ['OPENAI_API_KEY']
    
    
    def get_model(api_choice):
        if api_choice.lower() == "openai":
            return ChatOpenAI(model_name="gpt-4o",api_key=OPEN_API_KEY)
        elif api_choice.lower() == "gemini":
            return ChatGoogleGenerativeAI(model="gemini-pro")
        else:
            raise ValueError("Escolha inválida. Use 'openai' ou 'gemini'.")

    
    def verificar_json(json_data):

        def verificar_atividade(atividade):
                required_keys = ["atividade", "local", "latitude", "longitude", "horario", "custo_aproximado"]
                for key in required_keys:
                    if key not in atividade:
                        return False, f"Falta a chave {key} na atividade."
                    if key in ["latitude", "longitude"]:
                        try:
                            float(atividade[key])
                        except ValueError:
                            return False, f"{key} deve ser um número."
                    if key == "custo_aproximado":
                        partes = atividade[key].split(" ")
                        if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                            return False, f"custo_aproximado deve estar no formato 'simbolo_moeda valor_em_número'."
                return True, ""
            
        def verificar_hospedagem(hospedagem):
            required_keys = ["nome", "localizacao", "latitude", "longitude", "preco_medio", "comodidades"]
            for key in required_keys:
                if key not in hospedagem:
                    return False, f"Falta a chave {key} na hospedagem."
                if key in ["latitude", "longitude"]:
                    try:
                        float(hospedagem[key])
                    except ValueError:
                        return False, f"{key} deve ser um número."
                if key == "preco_medio":
                    partes = hospedagem[key].split(" ")
                    if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                        return False, f"Preço Médio deve estar no formato 'simbolo_moeda valor_em_número'."
            return True, ""    
        
        def verificar_orcamento(orcamento):
            required_keys = ["media_das_hospedagens", "alimentacao", "ingressos", "transporte", "extras_compras", "total"]
            for key in required_keys:
                if key not in orcamento:
                    return False, f"Falta a chave {key} no orçamento."
                partes = orcamento[key].split(" ")
                if len(partes) != 2 or not partes[1].replace('.', '', 1).isdigit():
                    return False, f"{key} deve estar no formato 'simbolo_moeda valor_em_número'."
            return True, ""
        
        if "roteiro" not in json_data:
            return False, "Falta a chave 'roteiro' no JSON."
        
        required_keys = ["recomendacoes_hospedagem", "orcamento", "dicas_observacoes"]

        for key in required_keys:
            if key not in json_data["roteiro"]:
                return False, f"Falta a chave '{key}' no JSON."

        if "dias" not in json_data["roteiro"]:
            return False, "Falta a chave 'dias' no roteiro."
        
        for index, dia in enumerate(json_data["roteiro"]["dias"], start=1):
            if "data" not in dia[next(iter(dia))]:
                dia_numero = f"dia_{index}"
                return False, f"Falta a chave 'data' no Roteiro do {dia_numero}."

            for periodo in ["manha", "tarde", "noite"]:
                if periodo in dia[next(iter(dia))]:
                    for atividade in dia[next(iter(dia))][periodo]:
                        valido, msg = verificar_atividade(atividade)
                        if not valido:
                            return False, msg
        
        for hospedagem in json_data["roteiro"]["recomendacoes_hospedagem"]:
            valido, msg = verificar_hospedagem(hospedagem)
            if not valido:
                return False, msg
            
        valido, msg = verificar_orcamento(json_data["roteiro"]["orcamento"])
        if not valido:
            return False, msg
        
        if not all(key.isdigit() for key in json_data["roteiro"]["dicas_observacoes"]):
            return False, "As chaves em 'dicas_observacoes' devem ser números sequenciais."
        
        return True, "JSON válido."


    def criar_rota_viagem(llm, prompt_template, destinos_interesse, recomendacao_hospedagem, data_inicio, preferencias_atividades, orcamento_disponivel, necessidades_especiais):
        while True:
            chain = LLMChain(llm=llm, prompt=prompt_template)
            dados_viagem = {
                "destinos_interesse": destinos_interesse,
                "recomendacao_hospedagem": recomendacao_hospedagem,
                "data_inicio": data_inicio,
                "preferencias_atividades": preferencias_atividades,
                "orcamento_disponivel": orcamento_disponivel,
                "necessidades_especiais": necessidades_especiais
            }

            response = chain.run(dados_viagem)
            resultado, mensagem = verificar_json(json.loads(response))

            if resultado:
                return json.loads(response)
            # Temporário
            else:
                return json.loads(response)
                """print(f"Resultado inválido.\nErro: {mensagem}.\nTentando novamente...\n"")"""


    prompt_template = PromptTemplate(
        input_variables=[
            "destinos_interesse",
            "recomendacao_hospedagem",
            "data_inicio",
            "preferencias_atividades",
            "orcamento_disponivel",
            "necessidades_especiais"
        ],
        template=(
            """Você será um especialista em viagens, seu papel é criar roteiros de viagens a partir de algumas informações que serão informadas abaixo
            Escolha as atividades mais requisitadas e famosas daquela localidade
            Por favor, crie um roteiro de viagem detalhado com as seguintes informações:

            - Destinos de Interesse: , principais pontos turrísiticos, {destinos_interesse}
            - Recomendação de Hospedagem: {recomendacao_hospedagem}
            - Datas de viagem: {data_inicio}
            - Preferências de Atividades: {preferencias_atividades}
            - Orçamento Disponível: {orcamento_disponivel}
            - Necessidades Especiais: {necessidades_especiais}

            - Certifique-se que as atividades em horários próximos sejam relativamente próximas
            - Cerifique-se que haja mais de uma atividade em cada período do dia e organize de forma que todos os horários do dia estejam ocupados,
            as atividades devem começar as 9 horas e terminarem as 22 horas
            - Sugira restaurantes perto das localidades das atividades para o almoço e jantar
            - Sugira ao menos 3 recomendações de hospedagem
            - dia_n é o dia 1 ... até n, onde n é o dia final
            - Não retorne ```json``
            - Caso a atividade seja gratuita, utilize simbolo_moeda_local 0

            O JSON deve seguir a estrutura abaixo:
            {{
            "roteiro": {{
                "dias": [
                    "dia_n" {{
                    "data": "Data do dia n",
                    "manha": [
                        {{
                            "atividade": "Nome da atividade",
                            "local": "Local da atividade",
                            "latitude": "Latitude do local",
                            "longitude": "Longitude do local",
                            "horario": "Horário da atividade",
                            "custo_aproximado": "simbolo_moeda_local valor_em_número"
                        }},
                        ...
                        ]
                    "tarde": [
                        {{
                            "atividade": "Nome da atividade",
                            "local": "Local da atividade",
                            "latitude": "Latitude do local",
                            "longitude": "Longitude do local",
                            "horario": "Horário da atividade",
                            "custo_aproximado": "simbolo_moeda_local valor_em_número"
                        }},
                        ...
                        ]
                        "noite": [
                        {{
                            "atividade": "Nome da atividade",
                            "local": "Local da atividade",
                            "latitude": "Latitude do local",
                            "longitude": "Longitude do local",
                            "horario": "Horário da atividade",
                            "custo_aproximado": "simbolo_moeda_local valor_em_número"
                        }},
                        ...
                        ]
                    }},
                    ...
                ],
                "recomendacoes_hospedagem": [
                {{
                    "nome": "Nome da Hospedagem",
                    "localizacao": "Localização da hospedagem",
                    "latitude": "Latitude da hospedagem",
                    "longitude": "Longitude da hospedagem",
                    "preco_medio": "simbolo_moeda_local valor_em_número",
                    "comodidades": ["Comodidade 1", ..., "Comodidade n"]
                }},
                ],
                "orcamento": {{
                    "media_das_hospedagens": "simbolo_moeda_local valor_em_número",
                    "alimentacao": "simbolo_moeda_local valor_em_número",
                    "ingressos": "simbolo_moeda_local valor_em_número",
                    "transporte": "simbolo_moeda_local valor_em_número",
                    "extras_compras": "simbolo_moeda_local valor_em_número",
                    "total": "simbolo_moeda_local valor_em_número"
                }},
                "dicas_observacoes": {{
                    "1": "Dica ou observação 1",
                    "2": "Dica ou observação 2",
                    "3": "Dica ou observação 3",
                    "4": "Dica ou observação 4",
                    "5": "Dica ou observação 5"
                }}
            }}
        }}
        """
        )
    )
    
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
    json_rota
    
    response_data = {
        **json_rota,
        "status": "success"
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
