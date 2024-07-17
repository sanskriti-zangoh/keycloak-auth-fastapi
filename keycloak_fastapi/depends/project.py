from api.schemas.project import CreateProject
from database.session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Project
from fastapi import HTTPException, status
from uuid import UUID
from sqlmodel import select

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
                return data
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
    
async def update_project(project_id: UUID, project: CreateProject):
    """
    Update a project.

    Args:
        project_id (int): A project id.
        project (CreateProject): A project.

    Returns:
        Project: A project.
    """
    try:
        async with get_db_session() as session:
            data = await session.execute(select(Project).where(Project.id == project_id))
            data = data.scalar_one_or_none()
            if data:
                data.name = project.name
                data.description = project.description
                await session.commit()
                return data
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
    
async def get_project_by_id(project_id: UUID):
    """
    Get a project by id.

    Args:
        project_id (int): A project id.

    Returns:
        Project: A project.
    """
    try:
        async with get_db_session() as session:
            data = await session.execute(select(Project).where(Project.id == project_id))
            data = data.scalar_one_or_none()
            return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
async def get_project_role_name(project_id: UUID):
    """
    Create a project role name.

    Args:
        project_id (int): A project id.

    Returns:
        str: A project role name.
    """
    role_name = "project-owner-" + str(project_id)
    return role_name

async def get_project_role_description(project_id: UUID):
    """
    Create a project role description.

    Args:
        project_id (int): A project id.

    Returns:
        str: A project role description.
    """
    role_description = "Project owner role for project " + str(project_id)
    return role_description