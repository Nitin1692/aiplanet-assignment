import { useState, useEffect } from "react";
import api from "../api/client";

interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

interface Workflow {
  id: number;
  name: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<number | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(null);

  // Fetch workflows for dropdown
  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const res = await api.get("/workflows/");
        setWorkflows(res.data.workflows);
        if (res.data.workflows.length > 0) {
          setSelectedWorkflow(res.data.workflows[0].id); // default first workflow
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchWorkflows();
  }, []);

  // Create a chat session whenever selectedWorkflow changes
  useEffect(() => {
    if (!selectedWorkflow) return;

    const createSession = async () => {
      try {
        const res = await api.post(`/chat/session/${selectedWorkflow}`);
        const newSessionId = res.data.session_id;
        setSessionId(newSessionId);
        setMessages([]); // clear previous messages
        fetchMessages(newSessionId); // load messages if any
      } catch (err) {
        console.error(err);
      }
    };

    createSession();
  }, [selectedWorkflow]);

  // Fetch messages for a session
  const fetchMessages = async (session: number) => {
    try {
      const res = await api.get(`/chat/session/${session}/messages`);
      setMessages(res.data.messages);
    } catch (err) {
      console.error(err);
    }
  };

  // Send a new message
  const sendMessage = async () => {
    if (!input.trim() || !sessionId) return;

    const newMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    try {
      // Post message to backend
      await api.post("/chat/message", {
        session_id: sessionId,
        role: "user",
        content: input,
      });

      // Call your AI backend to get the assistant's response
      const res = await api.post("/chat/query", {
        workflow_id: selectedWorkflow,
        query: input,
      });

      const reply: Message = { role: "assistant", content: res.data.answer };
      setMessages((prev) => [...prev, reply]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="chat-page" style={{ padding: "1rem" }}>
      {/* Workflow Selector */}
      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="workflow-select">Select Workflow: </label>
        <select
          id="workflow-select"
          value={selectedWorkflow ?? undefined}
          onChange={(e) => setSelectedWorkflow(Number(e.target.value))}
        >
          {workflows.map((wf) => (
            <option key={wf.id} value={wf.id}>
              {wf.name}
            </option>
          ))}
        </select>
      </div>

      {/* Chat Messages */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "1rem",
          height: "60vh",
          overflowY: "auto",
        }}
      >
        {messages.length === 0 ? (
          <p>No messages yet. Start the conversation!</p>
        ) : (
          messages.map((msg, i) => (
            <div key={i} style={{ margin: "0.5rem 0" }}>
              <strong>{msg.role === "user" ? "You" : "AI"}:</strong>{" "}
              {msg.content}
            </div>
          ))
        )}
      </div>

      {/* Input Box */}
      <div style={{ marginTop: "1rem" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: "80%", padding: "0.5rem" }}
          placeholder="Type your question..."
        />
        <button
          onClick={sendMessage}
          style={{ padding: "0.5rem 1rem", marginLeft: "0.5rem" }}
          disabled={!sessionId}
        >
          Send
        </button>
      </div>
    </div>
  );
}
