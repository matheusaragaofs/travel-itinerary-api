// Definição de tipos
export interface Atividade {
    atividade: string;
    local: string;
    horario: string;
    custo_aproximado: string;
  }
  
export type Periodo = 'manha' | 'tarde' | 'noite';
  
export interface Dia {
    data: string;
    manha: Atividade[];
    tarde: Atividade[];
    noite: Atividade[];
}
  
export interface Hospedagem {
    nome: string;
    localizacao: string;
    preco_medio: string;
    comodidades: string[];
}
  
export interface Orcamento {
    media_das_hospedagens: string;
    alimentacao: string;
    ingressos: string;
    transporte: string;
    extras_compras: string;
    total: string;
}
  
export interface DicasObservacoes {
    [key: number]: string;
}
  
export interface RoteiroResponse {
    roteiro: {
      dias: Dia[];
      recomendacoes_hospedagem: Hospedagem[];
      orcamento: Orcamento;
      dicas_observacoes: DicasObservacoes;
    };
}
  
export interface ApiRequestBody {
    destinos_interesse: string;
    recomendacao_hospedagem: string;
    data_inicio: string;
    preferencias_atividades: string;
    orcamento_disponivel: string;
    necessidades_especiais: string;
    apiKeyOpenAI: string;
    apiKeyGoogleMaps: string;
}