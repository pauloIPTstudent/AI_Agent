from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI()

# CONFIGURAÇÃO DE CORS: Permite que o Next.js (porta 3000) acesse o FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para a mensagem
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(data: ChatMessage):
    user_input = data.message
    
    # Chamada ao Ollama (usando o modelo phi3 ou o que você tiver no 'ollama list')
    # O 'system' prompt garante as respostas curtas que você pediu
    response = ollama.chat(model='phi3', messages=[
        {
            'role': 'system',
            'content': 'Responda sempre de forma muito curta, direta e objetiva.',
        },
        {
            'role': 'user',
            'content': user_input,
        },
    ])
    
    bot_reply = response['message']['content']
    
    return {"reply": bot_reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)