"use client"
import dynamic from 'next/dynamic'
import Dashboard from '@/components/DashBoard'
import 'react-chatbot-kit/build/main.css'
import config from './config';
import MessageParser from './MessageParser';
import ActionProvider from './ActionProvider';

const ChatbotSSRFree = dynamic(
  () => import('react-chatbot-kit').then((mod) => mod.default),
  { ssr: false }
)



export default function MainPage() {
  return (
    <main className="flex h-screen w-full overflow-hidden bg-white">
      
      {/* 1. Coluna do Conteúdo à ESQUERDA (flex-1 ocupa o resto do espaço) */}
      <Dashboard />

      {/* 2. Coluna do Chat fixa à DIREITA */}
      <aside className="w-[350px] h-full border-l border-gray-200 flex-shrink-0">
        <ChatbotSSRFree
          config={config}
          messageParser={MessageParser}
          actionProvider={ActionProvider}
        />
      </aside>

    </main>
  );
}