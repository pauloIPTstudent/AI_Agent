"use client"
import React, { useState, useEffect } from 'react';
import ReusableTable from './ReusableTable';

export default function Dashboard() {
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  // 1. Definição das colunas baseada no seu JSON
  const columns = [
    {key : 'id', label: 'ID'},
    { key: 'original_timestamp', label: 'Data/Hora' },
    { key: 'original_text', label: 'Texto Original' },
  ];

  // 2. Busca dos dados na API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/interactions_all');
        const data = await response.json();
        
        // Formatação simples da data para não ficar muito longa na tabela
        const formattedData = data.map(item => ({
          ...item,
          original_timestamp: new Date(item.original_timestamp).toLocaleString('pt-BR')
        }));

        setInteractions(formattedData);
      } catch (error) {
        console.error("Erro ao buscar interações:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

const handleRowClick = async (row) => {
    try {
      // Faz a requisição para o endpoint específico usando o ID da linha clicada
      const response = await fetch(`http://localhost:8000/interaction_by_id/${row.id}`);
      if (!response.ok) throw new Error("Erro ao buscar detalhes");
      const details = await response.json();

      // Monta uma string organizada para o alert
      const message = `
        DETALHES DA INTERAÇÃO (ID: ${details.id})
        -----------------------------------------
        Pergunta Original: ${details.original_text}
        Data: ${new Date(details.original_timestamp).toLocaleString('pt-BR')}\n
        Refinamento (model = ${details.refined_model}):
        "${details.refined_text}"\n
        Resposta Final (model = ${details.final_model}):
        "${details.final_text}"
      `;

      alert(message);
      
    } catch (error) {
      console.error("Erro:", error);
      alert("Não foi possível carregar os detalhes desta interação.");
    }
  };
  return (
    <section className="flex-1 h-full overflow-y-auto p-8 bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Painel de Controle Maestro</h1>
        
        <div className="grid grid-cols-2 gap-6">
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h2 className="font-semibold mb-2">Status do Grafo</h2>
            <p className="text-sm text-gray-500">LangGraph está aguardando conexão...</p>
          </div>
          <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h2 className="font-semibold mb-2">Logs da LLM</h2>
            <p className="text-sm text-gray-500">Nenhum evento processado.</p>
          </div>

       </div>
        <div className="mt-8 px-4 py-6 bg-white rounded-xl shadow-sm border border-gray-100 ">
            <h2 className="font-semibold mb-4 pl-2">Log de Interações</h2>
          {loading ? (
          <div className="flex justify-center p-10 text-gray-400">Carregando dados...</div>
        ) : (
          <ReusableTable 
            data={interactions} 
            columns={columns} 
            onRowClick={handleRowClick} 
          />
        )}
        </div>
      </div>
    </section>
  );
}