import json
from langchain.chains import LLMChain
from services.validation import verificar_json

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
        else:
            return json.loads(response)
