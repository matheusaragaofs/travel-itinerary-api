export const promptTemplate = `
Você será um especialista em viagens, seu papel é criar roteiros de viagens a partir de algumas informações que serão informadas abaixo
Escolha as atividades mais requisitadas e famosas daquela localidade
Por favor, crie um roteiro de viagem detalhado com as seguintes informações:

- Destinos de Interesse: {destinos_interesse}
- Recomendação de Hospedagem: {recomendacao_hospedagem}
- Datas de viagem: {data_inicio}
- Preferências de Atividades: {preferencias_atividades}
- Orçamento Disponível: {orcamento_disponivel}
- Necessidades Especiais: {necessidades_especiais}

- Certifique-se que as atividades em horários próximos sejam relativamente próximas
- Certifique-se que haja mais de uma atividade em cada período do dia e organize de forma que todos os horários do dia estejam ocupados,
as atividades devem começar às 9 horas e terminarem às 22 horas
- Sugira restaurantes perto das localidades das atividades para o almoço e jantar
- Sugira ao menos 3 recomendações de hospedagem
- dia_n é o dia 1 ... até n, onde n é o dia final
- Não retorne \`\`\`json\`\`\`
- Caso a atividade seja gratuita, utilize simbolo_moeda_local 0

O JSON deve seguir a estrutura abaixo:
{
  "roteiro": {
    "dias": [
        {
          "dia_n": {
            "data": "Data do dia n",
            "manha": [
                {
                  "atividade": "Nome da atividade",
                  "local": "Localização da atividade",
                  "horario": "Horário da atividade",
                  "custo_aproximado": "simbolo_moeda_local valor_em_número"
                }
                ...
              ],
            "tarde": [
                {
                  "atividade": "Nome da atividade",
                  "local": "Localização da atividade",
                  "horario": "Horário da atividade",
                  "custo_aproximado": "simbolo_moeda_local valor_em_número"
                }
                ...
              ],
            "noite": [
                {
                  "atividade": "Nome da atividade",
                  "local": "Localização da atividade",
                  "horario": "Horário da atividade",
                  "custo_aproximado": "simbolo_moeda_local valor_em_número"
                }
                ...
              ]
          }
        }
        ...
    ],
    "recomendacoes_hospedagem": [
      {
        "nome": "Nome da Hospedagem",
        "localizacao": "Localização da hospedagem",
        "preco_medio": "simbolo_moeda_local valor_em_número",
        "comodidades": ["Comodidade 1", ..., "Comodidade n"]
      }
    ],
    "orcamento": {
        "media_das_hospedagens": "simbolo_moeda_local valor_em_número",
        "alimentacao": "simbolo_moeda_local valor_em_número",
        "ingressos": "simbolo_moeda_local valor_em_número",
        "transporte": "simbolo_moeda_local valor_em_número",
        "extras_compras": "simbolo_moeda_local valor_em_número",
        "total": "simbolo_moeda_local valor_em_número"
    },
    "dicas_observacoes": {
        "1": "Dica ou observação 1",
        "2": "Dica ou observação 2",
        "3": "Dica ou observação 3",
        "4": "Dica ou observação 4",
        "5": "Dica ou observação 5"
    }
  }
}
`;