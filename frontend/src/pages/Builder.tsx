import { useCallback } from "react";
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useEdgesState,
  useNodesState,
} from "reactflow";
import type { Connection, Edge, Node } from "reactflow"; // ✅ type-only import
import "reactflow/dist/style.css";

const initialNodes: Node[] = [
  { id: "1", type: "input", position: { x: 250, y: 0 }, data: { label: "User Query" } },
];

const initialEdges: Edge[] = [];

export default function Builder() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes); // removed unused setNodes
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
