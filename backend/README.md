# Maestro AI Agent - Backend (FastAPI + Ollama)
Este é o servidor backend do projeto Maestro, responsável por gerenciar a lógica do Agente de IA, integração com LangGraph e comunicação com a LLM local via Ollama.

## 🛠️ Pré-requisitos
Antes de começar, certifique-se de ter instalado em sua máquina Linux:

Python 3.10 ou superior

Ollama (para rodar a LLM localmente)

Pip (gerenciador de pacotes Python)

## 📦 Dependências Principais
As bibliotecas essenciais utilizadas neste projeto são:

FastAPI: Framework web de alta performance.

Uvicorn: Servidor ASGI para rodar a aplicação.

Ollama: Biblioteca para integração com o motor de IA local.

Pydantic: Validação de dados e esquemas.

## 📥 Instalação
Siga os passos abaixo para configurar o ambiente:

Acesse a pasta do backend:

Bash
cd ~/AI_Agent/backend
Crie um ambiente virtual (VENV):

Bash
python3 -m venv venv
Ative o ambiente virtual:

Bash
source venv/bin/activate
Instale as dependências:

Bash
pip install -r requirements.txt

## 🧠 Configuração da IA (Ollama)
O backend depende do Ollama rodando no servidor.

Certifique-se de que o Ollama está ativo:

Bash
ollama serve
Baixe o modelo utilizado (ex: Llama 3):

Bash
ollama pull llama3
🚀 Como Rodar o Servidor
Com o ambiente virtual ativado, execute:

Bash
python3 main.py
O servidor iniciará por padrão em: http://localhost:8000

🔌 Endpoints Principais
POST /chat: Recebe uma mensagem do usuário e retorna a resposta da LLM.


Dica para Produção (Ngrok)
Para expor o backend para o frontend através de um túnel seguro:

Bash
ngrok http 8000