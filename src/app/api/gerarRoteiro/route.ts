import { NextResponse } from 'next/server';
import { OpenAI } from 'openai';
import { Client, GeocodeResponse } from '@googlemaps/google-maps-services-js';

const googleMapsClient = new Client({});

// Definição de tipos
interface Atividade {
  atividade: string;
  local: string;
  horario: string;
  custo_aproximado: string;
  latitude?: number;
  longitude?: number;
}

type Periodo = 'manha' | 'tarde' | 'noite';

interface Dia {
  data: string;
  manha: Atividade[];
  tarde: Atividade[];
  noite: Atividade[];
}

interface Hospedagem {
  nome: string;
  localizacao: string;
  preco_medio: string;
  comodidades: string[];
  latitude?: number;
  longitude?: number;
}

interface Orçamento {
  media_das_hospedagens: string;
  alimentacao: string;
  ingressos: string;
  transporte: string;
  extras_compras: string;
  total: string;
}

interface DicasObservacoes {
  [key: number]: string;
}

interface RoteiroResponse {
  roteiro: {
    dias: Dia[];
    recomendacoes_hospedagem: Hospedagem[];
    orcamento: Orçamento;
    dicas_observacoes: DicasObservacoes;
  };
}

interface ApiRequestBody {
  destinos_interesse: string;
  recomendacao_hospedagem: string;
  data_inicio: string;
  preferencias_atividades: string;
  orcamento_disponivel: string;
  necessidades_especiais: string;
  apiKeyOpenAI: string;
  apiKeyGoogleMaps: string;
}

const getLocaisFromDia = (dia: Dia): string[] => {
  const locais: string[] = [];
  const periodos: Periodo[] = ['manha', 'tarde', 'noite'];

  periodos.forEach(periodo => {
    const atividades = dia[periodo];
    if (atividades) {
      atividades.forEach(atividade => {
        locais.push(atividade.local);
      });
    }
  });

  return locais;
};

const promptTemplate = `
Você será um especialista em viagens, seu papel é criar roteiros de viagens a partir de algumas informações que serão informadas abaixo.
Escolha as atividades mais requisitadas e famosas daquela localidade e crie um roteiro detalhado.

Dados da Viagem:
- Destinos de Interesse: {destinos_interesse}
- Recomendação de Hospedagem: {recomendacao_hospedagem}
- Datas de viagem: {data_inicio}
- Preferências de Atividades: {preferencias_atividades}
- Orçamento Disponível: {orcamento_disponivel}
- Necessidades Especiais: {necessidades_especiais}

Instruções:
- Certifique-se que as atividades em horários próximos sejam relativamente próximas.
- Inclua pelo menos uma atividade em cada período do dia e organize de forma que todos os horários estejam ocupados, das 9h às 22h.
- Sugira restaurantes próximos às atividades para almoço e jantar.
- Sugira pelo menos 3 opções de hospedagem.
- Não retorne \`\`\`json\`\`\`.
- Caso a atividade seja gratuita, use simbolo_moeda_local 0.

Formato da Resposta:
{
  "roteiro": {
    "dias": [
      {
        "data": "Data do dia",
        "manha": [
          {
            "atividade": "Nome da atividade",
            "local": "Localização da atividade",
            "horario": "Horário da atividade",
            "custo_aproximado": "simbolo_moeda_local valor_em_número"
          }
        ],
        "tarde": [
          {
            "atividade": "Nome da atividade",
            "local": "Localização da atividade",
            "horario": "Horário da atividade",
            "custo_aproximado": "simbolo_moeda_local valor_em_número"
          }
        ],
        "noite": [
          {
            "atividade": "Nome da atividade",
            "local": "Localização da atividade",
            "horario": "Horário da atividade",
            "custo_aproximado": "simbolo_moeda_local valor_em_número"
          }
        ]
      }
    ],
    "recomendacoes_hospedagem": [
      {
        "nome": "Nome da Hospedagem",
        "localizacao": "Localização da hospedagem",
        "preco_medio": "simbolo_moeda_local valor_em_número",
        "comodidades": ["Comodidade 1", "Comodidade N"]
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

async function generateRoteiro(prompt: string, apiKey: string): Promise<RoteiroResponse> {
  const openai = new OpenAI({ apiKey });

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      functions: [{
        name: 'generateRoteiro',
        description: 'Gera um roteiro de viagem com a estrutura definida',
        parameters: {
          type: 'object',
          properties: {
            roteiro: {
              type: 'object',
              properties: {
                dias: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      data: { type: 'string' },
                      manha: {
                        type: 'array',
                        items: {
                          type: 'object',
                          properties: {
                            atividade: { type: 'string' },
                            local: { type: 'string' },
                            horario: { type: 'string' },
                            custo_aproximado: { type: 'string' },
                            latitude: { type: 'number', nullable: true },
                            longitude: { type: 'number', nullable: true }
                          },
                          required: ['atividade', 'local', 'horario', 'custo_aproximado']
                        }
                      },
                      tarde: {
                        type: 'array',
                        items: {
                          type: 'object',
                          properties: {
                            atividade: { type: 'string' },
                            local: { type: 'string' },
                            horario: { type: 'string' },
                            custo_aproximado: { type: 'string' },
                            latitude: { type: 'number', nullable: true },
                            longitude: { type: 'number', nullable: true }
                          },
                          required: ['atividade', 'local', 'horario', 'custo_aproximado']
                        }
                      },
                      noite: {
                        type: 'array',
                        items: {
                          type: 'object',
                          properties: {
                            atividade: { type: 'string' },
                            local: { type: 'string' },
                            horario: { type: 'string' },
                            custo_aproximado: { type: 'string' },
                            latitude: { type: 'number', nullable: true },
                            longitude: { type: 'number', nullable: true }
                          },
                          required: ['atividade', 'local', 'horario', 'custo_aproximado']
                        }
                      }
                    },
                    required: ['data', 'manha', 'tarde', 'noite']
                  }
                },
                recomendacoes_hospedagem: {
                  type: 'array',
                  items: {
                    type: 'object',
                    properties: {
                      nome: { type: 'string' },
                      localizacao: { type: 'string' },
                      preco_medio: { type: 'string' },
                      comodidades: { type: 'array', items: { type: 'string' } },
                      latitude: { type: 'number', nullable: true },
                      longitude: { type: 'number', nullable: true }
                    },
                    required: ['nome', 'localizacao', 'preco_medio', 'comodidades']
                  }
                },
                orcamento: {
                  type: 'object',
                  properties: {
                    media_das_hospedagens: { type: 'string' },
                    alimentacao: { type: 'string' },
                    ingressos: { type: 'string' },
                    transporte: { type: 'string' },
                    extras_compras: { type: 'string' },
                    total: { type: 'string' }
                  },
                  required: ['media_das_hospedagens', 'alimentacao', 'ingressos', 'transporte', 'extras_compras', 'total']
                },
                dicas_observacoes: {
                  type: 'object',
                  properties: {
                    '1': { type: 'string' },
                    '2': { type: 'string' },
                    '3': { type: 'string' },
                    '4': { type: 'string' },
                    '5': { type: 'string' }
                  }
                }
              },
              required: ['dias', 'recomendacoes_hospedagem', 'orcamento', 'dicas_observacoes']
            }
          }
        }
      }],
      function_call: { name: 'generateRoteiro' }
    });

    const respostaJson = response.choices[0]?.message?.function_call?.arguments;

    if (!respostaJson) {
      throw new Error('A resposta não está no formato esperado.');
    }

    return JSON.parse(respostaJson);
  } catch (error) {
    console.error('Erro ao gerar o roteiro:', error);
    throw error;
  }
}

export async function POST(request: Request) {
  const {
    destinos_interesse,
    recomendacao_hospedagem,
    data_inicio,
    preferencias_atividades,
    orcamento_disponivel,
    necessidades_especiais,
    apiKeyOpenAI,
    apiKeyGoogleMaps
  }: ApiRequestBody = await request.json();

  let tentativa = 0;
  let roteiroValido = false;
  let respostaJson: RoteiroResponse | null = null;

  while (tentativa < 3 && !roteiroValido) {
    tentativa++;
    let prompt = promptTemplate
      .replace('{destinos_interesse}', destinos_interesse)
      .replace('{recomendacao_hospedagem}', recomendacao_hospedagem)
      .replace('{data_inicio}', data_inicio)
      .replace('{preferencias_atividades}', preferencias_atividades)
      .replace('{orcamento_disponivel}', orcamento_disponivel)
      .replace('{necessidades_especiais}', necessidades_especiais);

    try {
      respostaJson = await generateRoteiro(prompt, apiKeyOpenAI);

      const locais: string[] = [];

      respostaJson.roteiro.dias.forEach(dia => {
        locais.push(...getLocaisFromDia(dia));
      });

      const validLocaisPromises = locais.map(local =>
        googleMapsClient.geocode({
          params: {
            address: local,
            key: apiKeyGoogleMaps
          }
        })
      );

      const validLocaisResponses: GeocodeResponse[] = await Promise.all(validLocaisPromises);

      respostaJson.roteiro.dias.forEach(dia => {
        dia.manha.forEach(atividade => {
          const localInfo = validLocaisResponses.find(response =>
            response.data.results[0]?.formatted_address === atividade.local
          );
          if (localInfo) {
            const { lat, lng } = localInfo.data.results[0]?.geometry.location || {};
            atividade.latitude = lat;
            atividade.longitude = lng;
          }
        });
        dia.tarde.forEach(atividade => {
          const localInfo = validLocaisResponses.find(response =>
            response.data.results[0]?.formatted_address === atividade.local
          );
          if (localInfo) {
            const { lat, lng } = localInfo.data.results[0]?.geometry.location || {};
            atividade.latitude = lat;
            atividade.longitude = lng;
          }
        });
        dia.noite.forEach(atividade => {
          const localInfo = validLocaisResponses.find(response =>
            response.data.results[0]?.formatted_address === atividade.local
          );
          if (localInfo) {
            const { lat, lng } = localInfo.data.results[0]?.geometry.location || {};
            atividade.latitude = lat;
            atividade.longitude = lng;
          }
        });
      });

      respostaJson.roteiro.recomendacoes_hospedagem.forEach(hospedagem => {
        const localInfo = validLocaisResponses.find(response =>
          response.data.results[0]?.formatted_address === hospedagem.localizacao
        );
        if (localInfo) {
          const { lat, lng } = localInfo.data.results[0]?.geometry.location || {};
          hospedagem.latitude = lat;
          hospedagem.longitude = lng;
        }
      });

      const todosLocaisValidos = locais.every(local =>
        validLocaisResponses.some(response =>
          response.data.results[0]?.formatted_address === local
        )
      );
      const locaisRepetidos = new Set(locais).size !== locais.length;

      if (todosLocaisValidos && !locaisRepetidos) {
        roteiroValido = true;
      } else {
        console.log("Atualizando o roteiro... ");
        prompt = `
          Atualize o roteiro gerado anteriormente, garantindo que todos os locais sejam válidos e não repetidos.
          Mantenha o contexto da viagem e gere novos locais válidos para qualquer local inválido ou repetido.
          O JSON deve seguir a estrutura abaixo:
          ${JSON.stringify(respostaJson, null, 2)}
        `;
      }
    } catch (error) {
      console.error('Erro ao gerar o roteiro:', error);
      if (tentativa >= 3) {
        return NextResponse.json({ error: 'Não foi possível gerar um roteiro válido após várias tentativas' }, { status: 400 });
      }
    }
  }

  if (!roteiroValido) {
    return NextResponse.json({ error: 'Não foi possível gerar um roteiro válido após várias tentativas' }, { status: 400 });
  }

  return NextResponse.json({ roteiro: respostaJson });
}
