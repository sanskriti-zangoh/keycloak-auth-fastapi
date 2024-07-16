from fastapi import APIRouter, Depends, HTTPException, status
from database.models import Project, ProjectType
from database.session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID

from api.schemas import (
    CreateProject
)

router = APIRouter(prefix="/project", tags=["project"])

@router.post("/")
async def create_project(project: CreateProject):
    """
    Create a project.

    Args:
        project (CreateProject): A project.

    Returns:
        Project: A project.
    """
    try:
        async with get_db_session() as session:
            new_project = Project(**project.model_dump())
            session.add(new_project)
            await session.flush()
        return new_project

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
@router.delete("/{project_id}")
async def delete_project(project_id: UUID):
    """
    Delete a project.

    Args:
        project_id (int): A project id.

    Returns:
        Project: A project.
    """
    try:
        async with get_db_session() as session:
            data = await session.execute(select(Project).where(Project.id == project_id))
            data = data.scalar_one_or_none()
            if data:
                await session.delete(data)
                return {
                    "message": "project is deleted",
                    "data": data
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="project not found"
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )