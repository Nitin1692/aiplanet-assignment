import { useEffect, useState } from "react";
import api from "../api/client";

interface Workflow {
  id: number;
  name: string;
  created_at: string;
  nodes?: any[]; // optional, if you want to pass to ReactFlow
  edges?: any[];
}

export default function Workflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);

  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const res = await api.get("/workflows/");
        // Backend returns { workflows: [...] }
        setWorkflows(res.data.workflows);
      } catch (err) {
        console.error(err);
      }
    };
    fetchWorkflows();
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Saved Workflows</h2>
      {workflows.length === 0 ? (
        <p>No workflows found.</p>
      ) : (
        <ul>
          {workflows.map((wf) => (
            <li key={wf.id}>
              {wf.name} ({new Date(wf.created_at).toLocaleString()})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
