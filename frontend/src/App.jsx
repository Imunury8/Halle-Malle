import React, { useState, useEffect, useRef } from 'react';
import './App.css';


function App() {
  const [inputText, setInputText] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isLoading]);

  // 💡 Colab에서 발급받은 Cloudflare 터널 주소로 변경하세요! (끝에 /ask 필수)
  const API_URL = "https://appliance-opera-nobody-neutral.trycloudflare.com/ask";

  const handleAsk = async () => {
    if (!inputText.trim()) return;

    // 사용자 질문 화면에 추가
    const newHistory = [...chatHistory, { role: "user", text: inputText }];
    setChatHistory(newHistory);
    setInputText("");
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_text: inputText }),
      });

      const data = await response.json();

      if (data.answer) {
        setChatHistory([...newHistory, { role: "coach", text: data.answer }]);
      } else if (data.error) {
        setChatHistory([...newHistory, { role: "error", text: `API 에러: ${data.error}` }]);
      }
    } catch (error) {
      setChatHistory([...newHistory, { role: "error", text: "서버 연결에 실패했습니다. Colab이 켜져 있는지 확인하세요." }]);
      console.error("Fetch Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <>
      <p className="subtitle">다이어트</p>
      <h1 className="title">할래말래</h1>

      <div className="chat relative overflow-hidden flex flex-col bg-white rounded-3xl shadow-lg p-6 chat-container">
        {/* 워터마크 */}
        <div
          className="absolute inset-0 flex items-center justify-center pointer-events-none select-none chat-watermark"
        >
          할래말래
        </div>

        {/* 채팅 메시지 영역 */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-4 custom-scrollbar relative z-10 w-full chat-messages-area">
          {chatHistory.length === 0 && (
            <div className="chat-empty-message">
              운동을 쉰 핑계를 대봐라
            </div>
          )}

          {chatHistory.map((msg, index) => (
            <div
              key={index}
              className={`flex flex-col chat-message-wrapper ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <span className="text-xs text-gray-500 mb-1 px-2 chat-message-sender">
                {msg.role === 'user' ? '사용자' : msg.role === 'error' ? '시스템' : '팩트코치'}
              </span>
              <div
                className={`max-w-[70%] px-4 py-3 rounded-2xl font-semibold whitespace-pre-wrap chat-message-bubble ${msg.role === 'user'
                  ? 'chat-bubble-user bg-[#5B4FE9] text-white'
                  : msg.role === 'error'
                    ? 'chat-bubble-error bg-red-100 text-red-800 border border-red-200'
                    : 'chat-bubble-coach bg-white text-gray-800 border border-gray-200'
                  }`}
              >
                {msg.role === 'error' ? `🚨 ${msg.text}` : msg.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex flex-col items-start chat-message-wrapper">
              <span className="text-xs text-gray-500 mb-1 px-2 chat-message-sender">팩트코치</span>
              <div
                className="max-w-[70%] px-4 py-3 rounded-2xl font-semibold bg-white text-gray-800 border border-gray-200 chat-message-bubble chat-bubble-coach chat-bubble-loading"
              >
                <div className="loading-spinner"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 입력 영역 */}
        <div className="flex gap-2 relative z-10 w-full chat-input-area">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyPress}
            disabled={isLoading}
            placeholder="운동을 쉰 핑계를 대봐라"
            className="flex-1 px-4 py-3 rounded-3xl border border-gray-100 focus:outline-none focus:ring-2 focus:ring-[#5B4FE9] resize-none min-h-[48px] max-h-[120px] chat-textarea"
            rows={1}
          />
          <button
            onClick={handleAsk}
            disabled={isLoading}
            className={`px-6 py-3 rounded-lg transition-colors text-white whitespace-nowrap chat-send-button ${isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-[#5B4FE9] hover:bg-[#4a3fd4]'
              }`}
          >
            전송
          </button>
        </div>
      </div>

    </>


  );

}

export default App;