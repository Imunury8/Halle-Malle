import { useState, useEffect, useRef } from 'react';

interface Message {
  id: number;
  text: string;
  sender: 'bot' | 'user';
  nickname?: string;
  time: string;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: '안녕하세요! 무엇을 도와드릴까요?', sender: 'bot', time: '10:00' },
    { id: 2, text: '안녕하세요!', sender: 'user', nickname: '사용자', time: '10:01' },
    { id: 3, text: '오늘 날씨가 어떤가요?', sender: 'user', nickname: '사용자', time: '10:02' },
    { id: 4, text: '오늘은 맑고 화창한 날씨입니다. 기온은 20도 정도로 쾌적합니다.', sender: 'bot', time: '10:03' },
    { id: 5, text: '감사합니다!', sender: 'user', nickname: '사용자', time: '10:04' },
  ]);

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (inputValue.trim() === '') return;

    const newMessage: Message = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      nickname: '사용자',
      time: new Date().toLocaleTimeString(),
    };

    setMessages([...messages, newMessage]);
    setInputValue('');

    // 챗봇 자동 응답 (예시)
    setTimeout(() => {
      const botResponse: Message = {
        id: messages.length + 2,
        text: '메시지를 받았습니다!',
        sender: 'bot',
        time: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, botResponse]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="size-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-2xl h-[600px] bg-white rounded-3xl shadow-lg flex flex-col p-6 relative overflow-hidden">
        {/* 워터마크 */}
        <div
          className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
          style={{
            fontFamily: "'Jua', sans-serif",
            fontSize: '7rem',
            fontWeight: '400',
            background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 50%, #ec4899 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            WebkitTextStroke: '2px rgba(139, 92, 246, 0.25)',
            textStroke: '2px rgba(139, 92, 246, 0.25)',
            letterSpacing: '0.05em',
            opacity: '0.15'
          }}
        >
          할래말래
        </div>

        {/* 채팅 메시지 영역 */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4 custom-scrollbar relative z-10">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex flex-col ${message.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <span className="text-xs text-gray-500 mb-1 px-2">
                {message.sender === 'user' ? message.nickname : '챗봇'}
              </span>
              <div
                className={`max-w-[50%] px-4 py-3 rounded-2xl font-semibold whitespace-pre-wrap ${
                  message.sender === 'user'
                    ? 'bg-[#5B4FE9] text-white'
                    : 'bg-white text-gray-800 border border-gray-200'
                }`}
                style={{
                  wordBreak: 'break-word',
                  overflowWrap: 'break-word',
                  whiteSpace: 'pre-wrap'
                }}
              >
                {message.text}
              </div>
              <span className="text-xs text-gray-500 mt-1 px-2">
                {message.time}
              </span>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* 입력 영역 */}
        <div className="flex gap-2 relative z-10">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="메시지를 입력하세요... (Shift+Enter: 줄바꿈)"
            className="flex-1 px-4 py-3 rounded-3xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-400 resize-none min-h-[48px] max-h-[120px]"
            rows={1}
          />
          <button
            onClick={handleSend}
            className="px-6 py-3 bg-[#5B4FE9] hover:bg-[#4a3fd4] text-white rounded-lg transition-colors"
          >
            전송
          </button>
        </div>
      </div>

      <style>{`
        .custom-scrollbar {
          scrollbar-width: thin;
          scrollbar-color: transparent transparent;
          transition: scrollbar-color 0.3s ease;
        }

        .custom-scrollbar:hover {
          scrollbar-color: #d1d5db transparent;
        }

        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }

        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }

        .custom-scrollbar::-webkit-scrollbar-thumb {
          background-color: transparent;
          border-radius: 20px;
          transition: background-color 0.3s ease;
        }

        .custom-scrollbar:hover::-webkit-scrollbar-thumb {
          background-color: #d1d5db;
        }
      `}</style>
    </div>
  );
}