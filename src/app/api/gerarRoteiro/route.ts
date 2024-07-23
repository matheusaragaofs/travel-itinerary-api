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
    if (atividades) { // Verifica se `atividades` não é `undefined`
      atividades.forEach(atividade => {
        locais.push(atividade.local);
      });
    }
  });

  return locais;
};

const promptTemplate = `
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

async function generateRoteiro(prompt: string, apiKey: string): Promise<string> {
  const openai = new OpenAI({ apiKey });

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: prompt }]
    });

    const content = response.choices[0]?.message.content;

    if (content === null || content === undefined) {
      throw new Error('O conteúdo da resposta é nulo ou indefinido.');
    }

    return content;

  } catch (error) {
    console.error('Erro ao gerar o roteiro:', error);
    throw error;
  }
}

export async function POST(request: Request): Promise<NextResponse> {
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

  // Verifica se as chaves das APIs foram fornecidas
  if (!apiKeyOpenAI || !apiKeyGoogleMaps) {
    return NextResponse.json({ error: 'API keys are required' }, { status: 400 });
  }

  let prompt = promptTemplate
    .replace('{destinos_interesse}', destinos_interesse)
    .replace('{recomendacao_hospedagem}', recomendacao_hospedagem)
    .replace('{data_inicio}', data_inicio)
    .replace('{preferencias_atividades}', preferencias_atividades)
    .replace('{orcamento_disponivel}', orcamento_disponivel)
    .replace('{necessidades_especiais}', necessidades_especiais);

  try {
    let roteiroValido = false;
    let respostaTexto = '';
    let tentativa = 0;

    while (!roteiroValido && tentativa < 3) {
      tentativa++;
      
      // Gera o roteiro com o OpenAI
      respostaTexto = await generateRoteiro(prompt, apiKeyOpenAI);
      
      // Analisa o JSON da resposta
      const respostaJson: RoteiroResponse = JSON.parse(respostaTexto);
      const locais: string[] = [];

      respostaJson.roteiro.dias.forEach(dia => {
        locais.push(...getLocaisFromDia(dia));
      });

      // Verifica a existência dos locais com a API do Google Maps
      const validLocaisPromises = locais.map(local =>
        googleMapsClient.geocode({
          params: {
            address: local,
            key: apiKeyGoogleMaps
          }
        })
      );

      const validLocaisResponses: GeocodeResponse[] = await Promise.all(validLocaisPromises);

      // Filtra apenas os locais válidos
      const validLocais = validLocaisResponses
        .filter(response => response.data.results.length > 0)
        .map(response => response.data.results[0].formatted_address);

      // Verifica se todos os locais são válidos e únicos
      const todosLocaisValidos = locais.every(local => validLocais.includes(local));
      const locaisRepetidos = new Set(locais).size !== locais.length;

      if (todosLocaisValidos && !locaisRepetidos) {
        roteiroValido = true;
      } else {
        // Atualiza o prompt para solicitar novos locais
        console.log("Atualizando o roteiro... ")
        prompt = `
          Atualize o roteiro gerado anteriormente, garantindo que todos os locais sejam válidos e não repetidos.
          Mantenha o contexto da viagem e gere novos locais válidos para qualquer local inválido ou repetido.
          O JSON deve seguir a estrutura abaixo:
          ${JSON.stringify(respostaJson, null, 2)}
        `;
      }
    }

    if (!roteiroValido) {
      return NextResponse.json({ error: 'Não foi possível gerar um roteiro válido após várias tentativas' }, { status: 400 });
    }

    return NextResponse.json({ roteiro: respostaTexto });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro ao gerar o roteiro' }, { status: 500 });
  }
}
