from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import TypedDict, List
import ollama
import uvicorn
from database.database import engine, SessionLocal, init_db, log_interaction
from database.models import UserMessage, RefinedMessage, FinalResponse

# 1. DEFINIÇÃO DO ESTADO DO AGENTE (Para o LangGraph)
class AgentState(TypedDict):
    user_input: str
    refined_prompt: str
    final_response: str

# 2. CONFIGURAÇÃO DOS CLIENTES
app = FastAPI()

# Permite que o Next.js fale com o FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com o Ollama Remoto via Ngrok
# Adicionado header para pular o aviso do ngrok que pode causar erros 10054
remote_client = ollama.Client(
    host='https://echoic-intransitive-berta.ngrok-free.dev',
    headers={'ngrok-skip-browser-warning': 'true'}
)

# 3. LÓGICA DO MAESTRO (NÓS DO GRAFO)
def prompt_optimizer(state: AgentState):
    """Nó que refina o prompt sem divagar e mantendo a brevidade."""
    user_msg = state['user_input']
    
    # Calculamos um limite baseado na mensagem original (ex: dobro do tamanho ou 150 caracteres)
    limit = len(user_msg) * 2
    
    response = remote_client.chat(
        model="phi3",
        messages=[
            {
                "role": "system", 
                "content": f"""Caso nescessário, corrija a frase abaixo para uma forma mais técnica e clara, removendo expressões coloquiais com um limite máximo de {limit} caracteres"""
            },
            {"role": "user", "content": f"{user_msg}"}
        ]
    )
    
    refined = response['message']['content'].strip()
    
    # Fallback de segurança: se ele divagar demais, usamos o original
    if len(refined) > (limit + 50):
        refined = user_msg
        
    print(f"--- [DEBUG] Prompt Otimizado: {refined} ---")
    return {"refined_prompt": refined}

def response_generator(state: AgentState):
    """Nó que gera a resposta final curta e objetiva."""
    response = remote_client.chat(
        model="phi3",
        messages=[
            {
                "role": "system", 
                "content": "Você é o Maestro. Responda de forma muito curta, direta e objetiva."
            },
            {"role": "user", "content": state['refined_prompt']}
        ]
    )
    return {"final_response": response['message']['content']}

# 4. CONSTRUÇÃO DO FLUXO (Manual ou via LangGraph)
# Para manter simples agora sem instalar muitas libs, simularemos o fluxo:
async def run_maestro_flow(message: str):
    # Passo 1: Otimizar
    state = {"user_input": message}
    optimized = prompt_optimizer(state)
    
    # Passo 2: Gerar Resposta
    state.update(optimized)
    result = response_generator(state)

    
    
    return result["final_response"]

# 5. ENDPOINT DA API
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatMessage):
    try:
        reply = await run_maestro_flow(data.message)
        return {"reply": reply}
    except Exception as e:
        print(f"Erro no fluxo Maestro: {e}")
        return {"reply": "Desculpe, tive um problema ao processar sua solicitação no servidor remoto."}

if __name__ == "__main__":
    # 1. Inicializa o banco de dados (Cria tabelas se não existirem)
    print("Inicializando banco de dados...")
    init_db()
    # 2. Inicia o servidor FastAPI
    print("Iniciando servidor FastAPI na porta 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)