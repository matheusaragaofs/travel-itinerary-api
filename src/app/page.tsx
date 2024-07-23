// app/page.tsx
'use client';

import { useState } from 'react';

export default function Home() {
  const [destinosInteresse, setDestinosInteresse] = useState('');
  const [recomendacaoHospedagem, setRecomendacaoHospedagem] = useState('');
  const [dataInicio, setDataInicio] = useState('');
  const [preferenciasAtividades, setPreferenciasAtividades] = useState('');
  const [orcamentoDisponivel, setOrcamentoDisponivel] = useState('');
  const [necessidadesEspeciais, setNecessidadesEspeciais] = useState('');
  const [apiKeyOpenAI, setApiKeyOpenAI] = useState('');
  const [apiKeyGoogleMaps, setApiKeyGoogleMaps] = useState('');

  const [roteiro, setRoteiro] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const response = await fetch('/api/gerarRoteiro', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        destinos_interesse: destinosInteresse,
        recomendacao_hospedagem: recomendacaoHospedagem,
        data_inicio: dataInicio,
        preferencias_atividades: preferenciasAtividades,
        orcamento_disponivel: orcamentoDisponivel,
        necessidades_especiais: necessidadesEspeciais,
        apiKeyOpenAI: apiKeyOpenAI,
        apiKeyGoogleMaps: apiKeyGoogleMaps
      }),
    });

    const data = await response.json();
    setRoteiro(data.roteiro);
  };

  return (
    <div>
      <h1>Gerador de Roteiro de Viagem</h1>
      <form onSubmit={handleSubmit}>
        <label>
          API OpenAI:
          <input
            type="text"
            value={apiKeyOpenAI}
            onChange={(e) => setApiKeyOpenAI(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          API GoogleMaps:
          <input
            type="text"
            value={apiKeyGoogleMaps}
            onChange={(e) => setApiKeyGoogleMaps(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Destinos de Interesse:
          <input
            type="text"
            value={destinosInteresse}
            onChange={(e) => setDestinosInteresse(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Recomendação de Hospedagem:
          <input
            type="text"
            value={recomendacaoHospedagem}
            onChange={(e) => setRecomendacaoHospedagem(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Datas:
          <input
            type="text"
            value={dataInicio}
            onChange={(e) => setDataInicio(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Preferências de Atividades:
          <input
            type="text"
            value={preferenciasAtividades}
            onChange={(e) => setPreferenciasAtividades(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Orçamento Disponível:
          <input
            type="text"
            value={orcamentoDisponivel}
            onChange={(e) => setOrcamentoDisponivel(e.target.value)}
          />
        </label>
        <br></br>
        <label>
          Necessidades Especiais:
          <input
            type="text"
            value={necessidadesEspeciais}
            onChange={(e) => setNecessidadesEspeciais(e.target.value)}
          />
        </label>
        <br></br>
        <button type="submit">Gerar Roteiro</button>
      </form>

      {roteiro && (
        <div>
          <h2>Roteiro Gerado:</h2>
          <pre>{roteiro}</pre>
        </div>
      )}
    </div>
  );
}
