import { createChatBotMessage } from 'react-chatbot-kit';

const config = {
  initialMessages: [createChatBotMessage(`Olá! Sou seu assistente TagusValleyBot. Como posso ajudar?`, {})],
  botName: "TagusValleyBot",
  customStyles: {
    botMessageBox: { backgroundColor: '#000' },
    chatButton: { backgroundColor: '#000' },
  },
};

export default config;