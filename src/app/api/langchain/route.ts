import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { ChatOpenAI } from "@langchain/openai";
import { PromptTemplate } from "@langchain/core/prompts";

const TEMPLATE = `Você será um especialista em viagens, seu papel é criar roteiros de viagens a partir de algumas informações que serão informadas abaixo
Escolha as atividades mais requisitadas e famosas daquela localidade
Por favor, crie um roteiro de viagem detalhado com as seguintes informações:

- Destinos de Interesse: , principais pontos turísticos, {destinos_interesse}
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
- Não retorne \`\`\`json\`\`\`
- Caso a atividade seja gratuita, utilize simbolo_moeda_local 0

O JSON deve seguir a estrutura abaixo:
{
  "roteiro": {
    "dias": [
        "dia_n" {
          "data": "Data do dia n",
          "manha": [
              {
                "atividade": "Nome da atividade",
                "local": "Local da atividade",
                "latitude": "Latitude do local",
                "longitude": "Longitude do local",
                "horario": "Horário da atividade",
                "custo_aproximado": "simbolo_moeda_local valor_em_número"
              },
              ...
            ]
          "tarde": [
              {
                "atividade": "Nome da atividade",
                "local": "Local da atividade",
                "latitude": "Latitude do local",
                "longitude": "Longitude do local",
                "horario": "Horário da atividade",
                "custo_aproximado": "simbolo_moeda_local valor_em_número"
              },
              ...
            ]
            "noite": [
              {
                "atividade": "Nome da atividade",
                "local": "Local da atividade",
                "latitude": "Latitude do local",
                "longitude": "Longitude do local",
                "horario": "Horário da atividade",
                "custo_aproximado": "simbolo_moeda_local valor_em_número"
              },
              ...
            ]
        },
        ...
    ],
    "recomendacoes_hospedagem": [
      {
        "nome": "Nome da Hospedagem",
        "localizacao": "Localização da hospedagem",
        "latitude": "Latitude da hospedagem",
        "longitude": "Longitude da hospedagem",
        "preco_medio": "simbolo_moeda_local valor_em_número",
        "comodidades": ["Comodidade 1", ..., "Comodidade n"]
      },
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
}`;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      apiKey,
      destinos_interesse,
      recomendacao_hospedagem,
      data_inicio,
      preferencias_atividades,
      orcamento_disponivel,
      necessidades_especiais
    } = body;

    if (!apiKey) {
      return NextResponse.json({ error: 'API key is required' }, { status: 400 });
    }

    const prompt = PromptTemplate.fromTemplate(TEMPLATE);

    const model = new ChatOpenAI({
      apiKey: apiKey,
      model: "gpt-4o"
    });

    console.log(apiKey,
      destinos_interesse,
      recomendacao_hospedagem,
      data_inicio,
      preferencias_atividades,
      orcamento_disponivel,
      necessidades_especiais)

    const schema = z
      .object({
        roteiro: z.object({
          dias: z.array(
            z.object({
              data: z.string(),
              manha: z.array(
                z.object({
                  atividade: z.string(),
                  local: z.string(),
                  latitude: z.string(),
                  longitude: z.string(),
                  horario: z.string(),
                  custo_aproximado: z.string(),
                })
              ),
              tarde: z.array(
                z.object({
                  atividade: z.string(),
                  local: z.string(),
                  latitude: z.string(),
                  longitude: z.string(),
                  horario: z.string(),
                  custo_aproximado: z.string(),
                })
              ),
              noite: z.array(
                z.object({
                  atividade: z.string(),
                  local: z.string(),
                  latitude: z.string(),
                  longitude: z.string(),
                  horario: z.string(),
                  custo_aproximado: z.string(),
                })
              ),
            })
          ),
          recomendacoes_hospedagem: z.array(
            z.object({
              nome: z.string(),
              localizacao: z.string(),
              latitude: z.string(),
              longitude: z.string(),
              preco_medio: z.string(),
              comodidades: z.array(z.string()),
            })
          ),
          orcamento: z.object({
            media_das_hospedagens: z.string(),
            alimentacao: z.string(),
            ingressos: z.string(),
            transporte: z.string(),
            extras_compras: z.string(),
            total: z.string(),
          }),
          dicas_observacoes: z.object({
            1: z.string(),
            2: z.string(),
            3: z.string(),
            4: z.string(),
            5: z.string(),
          }),
        }),
      })
      .describe('Should always be used to properly format output');

    const functionCallingModel = model.withStructuredOutput(schema, {
      name: 'output_formatter',
    });

    const chain = prompt.pipe(functionCallingModel);

    const input = {
      destinos_interesse,
      recomendacao_hospedagem,
      data_inicio,
      preferencias_atividades,
      orcamento_disponivel,
      necessidades_especiais,
    };

    const result = await chain.invoke(input);

    return NextResponse.json(result, { status: 200 });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: e.status ?? 500 });
  }
}