import React from "react";

const components = ["User Query", "LLM", "Knowledge Base", "API"];

export default function Sidebar() {
  const onDragStart = (event: React.DragEvent, component: string) => {
    event.dataTransfer.setData("application/reactflow", component);
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <aside
      style={{
        width: "220px",
        background: "#1b1a1aff",
        borderRight: "1px solid #ddd",
        padding: "1rem",
        height: "100vh",
      }}
    >
      <h3 style={{ marginBottom: "1rem" }}>Component Library</h3>
      {components.map((comp) => (
        <div
          key={comp}
          draggable
          onDragStart={(e) => onDragStart(e, comp)}
          style={{
            padding: "8px",
            marginBottom: "8px",
            background: "black",
            border: "1px solid #fff",
            borderRadius: "4px",
            cursor: "grab",
          }}
        >
          {comp}
        </div>
      ))}
    </aside>
  );
}
