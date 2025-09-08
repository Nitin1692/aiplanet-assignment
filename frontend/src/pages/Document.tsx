import { useState } from "react";
import api from "../api/client";

export default function Documents() {
  const [file, setFile] = useState<File | null>(null);
  const [docs, setDocs] = useState<any[]>([]);

  const uploadDoc = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("Uploaded!");
      setDocs((prev) => [...prev, res.data]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Knowledge Base Documents</h2>
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button onClick={uploadDoc} style={{ marginLeft: "0.5rem" }}>
        Upload
      </button>

      <ul>
        {docs.map((d, i) => (
          <li key={i}>{d.filename}</li>
        ))}
      </ul>
    </div>
  );
}
