import Sidebar from "../components/sidebar";
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useEdgesState,
  useNodesState,
} from "reactflow";
import type { Connection, Edge } from "reactflow";
import "reactflow/dist/style.css";
import { useCallback, useState } from "react";
import axios from "axios";
import api from "../api/client";

export default function Builder() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [saving, setSaving] = useState(false);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();
      const component = event.dataTransfer.getData("application/reactflow");

      const position = reactFlowInstance.project({
        x: event.clientX - 250, // offset because of sidebar width
        y: event.clientY,
      });

      const newNode = {
        id: `${+new Date()}`,
        type: "default",
        position,
        data: { label: component },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  const onDragOver = (event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  // -----------------------------
  // Save workflow to backend
  // -----------------------------
  const saveWorkflow = async () => {
    if (!reactFlowInstance) return;

    setSaving(true);
    try {
      const workflowName = prompt("Enter workflow name:");
      if (!workflowName) return;

      const response = await api.post("/workflows/", {
        name: workflowName,
        nodes: nodes,
        edges: edges,
      });

      alert(`Workflow saved with ID: ${response.data.id}`);
    } catch (error: any) {
      console.error(error);
      alert("Failed to save workflow");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", width: "100%" }}>
      {/* Sidebar */}
      <Sidebar />

      {/* Canvas */}
      <div
        style={{ flex: 1, position: "relative" }}
        onDrop={onDrop}
        onDragOver={onDragOver}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          onInit={setReactFlowInstance}
        >
          <Background />
          <Controls />
        </ReactFlow>

        {/* Save Workflow Button */}
        <button
          onClick={saveWorkflow}
          disabled={saving}
          style={{
            position: "absolute",
            right: 20,
            top: 20,
            zIndex: 10,
          }}
        >
          {saving ? "Saving..." : "Save Workflow"}
        </button>
      </div>
    </div>
  );
}
