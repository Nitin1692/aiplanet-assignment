import { useState } from "react";
import api from "../api/client";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    try {
      const res = await api.post("/chat/query", {
        query: input,
        workflow_id: 1, // later make dynamic
      });

      const reply: Message = { role: "assistant", content: res.data.answer };
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-page" style={{ padding: "1rem" }}>
      <div style={{ border: "1px solid #ccc", padding: "1rem", height: "70vh", overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ margin: "0.5rem 0" }}>
            <strong>{msg.role === "user" ? "You" : "AI"}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div style={{ marginTop: "1rem" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: "80%", padding: "0.5rem" }}
          placeholder="Type your question..."
        />
        <button onClick={sendMessage} style={{ padding: "0.5rem 1rem", marginLeft: "0.5rem" }}>
          Send
        </button>
      </div>
    </div>
  );
}
