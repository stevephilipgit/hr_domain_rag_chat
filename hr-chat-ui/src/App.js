import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [typing, setTyping] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userText = message;
    setChat((prev) => [...prev, { role: "user", text: userText }]);
    setMessage("");
    setTyping(true);

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: "demo-session",
        message: userText,
      }),
    });

    const data = await res.json();
    setTyping(false);

    setChat((prev) => [
      ...prev,
      {
        role: "bot",
        text: data.answer,
        sources: data.sources,
      },
    ]);
  };

  return (
    <div className="chat-container">
      <h2>HR Chatbot</h2>

      <div className="chat-box">
        {chat.map((c, i) => (
          <div key={i} className={c.role === "user" ? "user-msg" : "bot-msg"}>
            <div
              className={`bubble ${
                c.role === "user" ? "user-bubble" : "bot-bubble"
              }`}
            >
              {c.role === "bot" ? (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {c.text}
                </ReactMarkdown>
              ) : (
                c.text
              )}

              {c.role === "bot" && c.sources?.length > 0 && (
                <div className="sources">
                  <b>Sources:</b>
                  <ul>
                    {c.sources.map((s, idx) => (
                      <li key={idx}>
                        {s.source.split("\\").pop()} — page {s.page}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {typing && (
          <div className="bot-msg">
            <div className="bubble bot-bubble typing">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
      </div>

      <div style={{ display: "flex", marginTop: 10 }}>
        <input
          style={{ flex: 1, padding: 10 }}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a question..."
        />
        <button onClick={sendMessage} style={{ padding: "10px 16px" }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
