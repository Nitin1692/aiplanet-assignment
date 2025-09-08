import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Builder from "./pages/Builder";
import Chat from "./pages/Chat";
import Documents from "./pages/Document";
import Workflows from "./pages/Workflow";

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
        <Link to="/">Builder</Link> |{" "}
        <Link to="/chat">Chat</Link> |{" "}
        <Link to="/documents">Documents</Link> |{" "}
        <Link to="/workflows">Workflows</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Builder />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/workflows" element={<Workflows />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
