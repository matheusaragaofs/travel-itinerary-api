import { NextResponse } from 'next/server';
import { OpenAI } from 'openai';
import { Client, GeocodeResponse } from '@googlemaps/google-maps-services-js';
import { promptTemplate } from '../templates/prompTemplate';
import { Atividade, Periodo, Dia, Hospedagem, Orcamento, DicasObservacoes, RoteiroResponse, ApiRequestBody } from '../templates/types';

const googleMapsClient = new Client({});

// Funcao para pegar todos os locais dos roteiros
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

// Funcao para gerar o roteiro, fazendo a requisiao para a openAI
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

// Funcao POST que o front realiza a reuqisição, ela é a "main"
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
