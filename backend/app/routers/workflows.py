from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import create_workflow, get_workflows, get_connection
from typing import List, Dict, Any

router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


@router.post("/")
def add_workflow(workflow: WorkflowCreate):
    workflow_id = create_workflow(workflow.name, workflow.nodes, workflow.edges)
    return {"id": workflow_id, "message": "Workflow created successfully"}


@router.get("/")
def list_workflows():
    rows = get_workflows()
    workflows = [
        {
            "id": row["id"],
            "name": row["name"],
            "nodes": row["nodes"],  # Already JSON
            "edges": row["edges"],  # Already JSON
            "created_at": row["created_at"]
        }
        for row in rows
    ]
    return {"workflows": workflows}



@router.put("/{workflow_id}")
def update_workflow(workflow_id: int, workflow: WorkflowCreate):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """UPDATE workflows
               SET name = %s, nodes = %s, edges = %s
               WHERE id = %s RETURNING id;""",
            (workflow.name, workflow.nodes, workflow.edges, workflow_id)
        )
        updated = cur.fetchone()
        conn.commit()
        if not updated:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return {"message": "Workflow updated successfully"}
    finally:
        cur.close()
        conn.close()


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM workflows WHERE id = %s RETURNING id;", (workflow_id,))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return {"message": "Workflow deleted successfully"}
    finally:
        cur.close()
        conn.close()
