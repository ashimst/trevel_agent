import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User as UserIcon } from 'lucide-react';
import { sendChatMessage } from '../api/services.js';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

export default function ChatPage() {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('yatra_messages');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error("Failed to parse saved chat messages:", e);
      }
    }
    const defaultMsg = { 
      id: '1', 
      role: 'ai', 
      content: 'Hello! I\'m **Yatra**, your AI travel concierge. I can search for flights, hotels, buses, activities, guides, and car rentals. I can also book, manage your bookings, and organize trips for you.\n\nWhat would you like to do today?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    return [defaultMsg];
  });
  
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState(() => localStorage.getItem('yatra_thread_id'));
  const messagesEndRef = useRef(null);

  const startNewChat = () => {
    localStorage.removeItem('yatra_thread_id');
    localStorage.removeItem('yatra_messages');
    setThreadId(null);
    const defaultMsg = { 
      id: '1', 
      role: 'ai', 
      content: 'Hello! I\'m **Yatra**, your AI travel concierge. I can search for flights, hotels, buses, activities, guides, and car rentals. I can also book, manage your bookings, and organize trips for you.\n\nWhat would you like to do today?',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages([defaultMsg]);
  };

  useEffect(() => {
    localStorage.setItem('yatra_messages', JSON.stringify(messages));
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg = { id: Date.now().toString(), role: 'user', content: input, timestamp: timeStr };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendChatMessage(userMsg.content, threadId);
      if (!threadId) {
        setThreadId(data.thread_id);
        localStorage.setItem('yatra_thread_id', data.thread_id);
      }
      const aiTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages(prev => [...prev, { 
        id: (Date.now() + 1).toString(), 
        role: 'ai', 
        content: data.response,
        timestamp: aiTimeStr
      }]);
    } catch {
      const aiTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages(prev => [...prev, { 
        id: (Date.now() + 1).toString(), 
        role: 'ai', 
        content: 'I apologize, but I encountered an error processing your request.',
        timestamp: aiTimeStr
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container glass-panel" style={{ overflow: 'hidden' }}>
      <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '1.1rem' }}>Ask Yatra AI</h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Search, book, manage bookings &amp; trips — powered by AI
          </p>
        </div>
        <button onClick={startNewChat} className="btn" style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}>
          New Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <motion.div key={msg.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            className={`message-row ${msg.role}`}>
            <div className={`message-avatar ${msg.role}`}>
              {msg.role === 'user' ? <UserIcon size={18} /> : <Bot size={18} />}
            </div>
            
            <div style={{ 
              display: 'flex', 
              flexDirection: 'column', 
              maxWidth: '80%', 
              alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' 
            }}>
              <div className={`message-bubble ${msg.role}`}>
                {msg.role === 'ai' ? (
                  <div className="markdown-body"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
                ) : msg.content}
              </div>
              {msg.timestamp && (
                <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: '4px', padding: '0 4px' }}>
                  {msg.timestamp}
                </span>
              )}
            </div>
          </motion.div>
        ))}

        {isLoading && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="message-row">
            <div className="message-avatar ai"><Bot size={18} /></div>
            <div className="loading-dots"><span /><span /><span /></div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.75rem' }}>
          <input type="text" className="input-field" placeholder="Ask Yatra anything about your travels..."
            value={input} onChange={(e) => setInput(e.target.value)}
            style={{ borderRadius: 'var(--radius-full)', paddingLeft: '1.5rem' }} />
          <button type="submit" className="btn btn-primary"
            style={{ borderRadius: '50%', width: '46px', height: '46px', padding: 0, flexShrink: 0 }}
            disabled={!input.trim() || isLoading}>
            <Send size={18} style={{ marginLeft: '-2px' }} />
          </button>
        </form>
      </div>
    </div>
  );
}
