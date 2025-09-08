import { useEffect, useState } from "react";
import api from "../api/client";

interface Workflow {
  id: number;
  name: string;
  created_at: string;
}

export default function Workflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);

  useEffect(() => {
    const fetchWorkflows = async () => {
      try {
        const res = await api.get("/workflows/");
        setWorkflows(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchWorkflows();
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Saved Workflows</h2>
      <ul>
        {workflows.map((wf) => (
          <li key={wf.id}>
            {wf.name} ({new Date(wf.created_at).toLocaleString()})
          </li>
        ))}
      </ul>
    </div>
  );
}
