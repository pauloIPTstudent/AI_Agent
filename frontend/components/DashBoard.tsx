export default function Dashboard() {
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

        <div className="mt-8 p-6 bg-white rounded-xl shadow-sm border border-gray-100 h-96 flex items-center justify-center">
           <p className="text-gray-400 italic">Área para visualização de dados, mapas ou gráficos.</p>
        </div>
      </div>
    </section>
  );
}