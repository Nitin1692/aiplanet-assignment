import { useState } from "react";
import api from "../api/client";

export default function Documents() {
  const [file, setFile] = useState<File | null>(null);
  const [collection, setCollection] = useState("default"); // collection input
  const [docs, setDocs] = useState<any[]>([]);

  const uploadDoc = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("collection", collection);

    try {
      const res = await api.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Uploaded!");
      setDocs((prev) => [...prev, res.data]);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Knowledge Base Documents</h2>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <input
          type="text"
          placeholder="Collection name"
          value={collection}
          onChange={(e) => setCollection(e.target.value)}
          style={{ marginLeft: "0.5rem" }}
        />
        <button onClick={uploadDoc} style={{ marginLeft: "0.5rem" }}>
          Upload
        </button>
      </div>

      <h3>Uploaded Documents</h3>
      <ul>
        {docs.map((d, i) => (
          <li key={i}>
            <strong>{d.filename}</strong> → Collection: {d.collection} ({d.chars} chars)
          </li>
        ))}
      </ul>
    </div>
  );
}
