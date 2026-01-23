class ActionProvider {
  createChatBotMessage: any;
  setState: any;

  constructor(createChatBotMessage: any, setStateFunc: any) {
    this.createChatBotMessage = createChatBotMessage;
    this.setState = setStateFunc;
  }

  handleUserMessage = async (message: string) => {
    try {
      // Chamada para o backend
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) throw new Error("Erro na rede");

      const data = await response.json();

      // Cria a mensagem do bot com o que veio do FastAPI
      const botMessage = this.createChatBotMessage(data.reply);

      this.updateChatbotState(botMessage);
    } catch (error) {
      const errorMessage = this.createChatBotMessage("Erro: Não consegui falar com o servidor.");
      this.updateChatbotState(errorMessage);
    }
  };

  updateChatbotState(message: any) {
    this.setState((prevState: any) => ({
      ...prevState,
      messages: [...prevState.messages, message],
    }));
  }
}

export default ActionProvider;