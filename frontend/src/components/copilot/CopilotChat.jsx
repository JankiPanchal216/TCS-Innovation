import React, { useState } from 'react';
import { Send, Sparkles } from 'lucide-react';
import { askCopilot } from '../../services/aiService';

const CopilotChat = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi! I'm your AI Copilot. Ask me anything about your learning path, book prerequisites, or syllabus alignment.", sender: 'ai' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { id: Date.now(), text: input, sender: 'user' };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await askCopilot(userMsg.text);
      setMessages(prev => [...prev, { id: Date.now() + 1, text: response.answer, sender: 'ai' }]);
    } catch (error) {
      setMessages(prev => [...prev, { id: Date.now() + 1, text: "Sorry, I'm having trouble connecting right now.", sender: 'ai' }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="bg-[#17152A] rounded-xl border border-[#3E3A5A] shadow-lg flex flex-col h-[600px] overflow-hidden">
      <div className="p-4 border-b border-white/10 flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-[#6D4AFF]" />
        <h3 className="font-bold text-white">Ask Copilot</h3>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-lg p-3 text-sm ${
              msg.sender === 'user' 
                ? 'bg-[#6D4AFF] text-white rounded-br-none' 
                : 'bg-white/10 text-white border border-white/10 rounded-bl-none'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white/10 text-white border border-white/10 rounded-lg rounded-bl-none p-3 flex gap-1">
              <span className="w-1.5 h-1.5 bg-white/50 rounded-full animate-bounce"></span>
              <span className="w-1.5 h-1.5 bg-white/50 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
              <span className="w-1.5 h-1.5 bg-white/50 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-white/5 border-t border-white/10">
        <form onSubmit={handleSend} className="relative">
          <input 
            type="text" 
            placeholder="Ask a question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="w-full bg-[#17152A] border border-white/20 rounded-full pl-4 pr-12 py-2.5 text-sm text-white focus:outline-none focus:border-[#6D4AFF] transition-colors"
          />
          <button 
            type="submit"
            disabled={!input.trim() || isTyping}
            className="absolute right-1 top-1 w-8 h-8 rounded-full bg-[#6D4AFF] flex items-center justify-center text-white disabled:opacity-50 transition-opacity"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default CopilotChat;
