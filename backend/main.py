from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.maestro import maestro_app
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
    # Invoca o LangGraph
    inputs = {"messages": [data.message]}
    result = maestro_app.invoke(inputs)
    
    # Pega a última mensagem gerada pelo grafo
    bot_reply = result["messages"][-1]
    
    return {"reply": bot_reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)