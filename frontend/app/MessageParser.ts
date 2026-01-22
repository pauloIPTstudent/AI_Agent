// MessageParser.ts
class MessageParser {
  actionProvider: any;

  constructor(actionProvider: any) {
    this.actionProvider = actionProvider;
  }

  parse(message: string) {
    const lowercaseMessage = message.toLowerCase();

    // Se a mensagem não estiver vazia, envia para o ActionProvider
    if (message.trim()) {
      this.actionProvider.handleUserMessage(message);
    }
  }
}

export default MessageParser;