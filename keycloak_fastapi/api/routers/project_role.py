from fastapi import APIRouter, Depends, HTTPException, status
from depends.auth import get_user_id, has_role_bool, get_payload
from depends.project import create_project, update_project, delete_project, get_project_role_name, get_project_role_description
from depends.roles import create_role, delete_role, assign_role, revoke_role

from uuid import UUID
from api.schemas import CreateProject
from database.models import Project, ProjectType

router = APIRouter(prefix="/project_role", tags=["project_role"])

@router.post("/")
async def create_project_and_role(project: CreateProject, user_id: UUID = Depends(get_user_id)):
    try:
        new_project = await create_project(project=project)
        role = await get_project_role_name(project_id=new_project.id)
        description = await get_project_role_description(project_id=new_project.id)
        await create_role(role_name=role, description=description)
        await assign_role(user_id=user_id, role_name=role)
        return {
            "message": "project is created",
            "data": new_project
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{project_id}")
async def update_project_with_role(
    project_id: UUID,
    project: CreateProject,
    token_data: dict = Depends(get_payload)
):
    # Dynamically generate the role name based on the project_id
    role_name = await get_project_role_name(project_id=project_id)
    print(role_name)

    # Check if the user has the role
    if not await has_role_bool(role_name)(token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have the required role to update this project"
        )
    
    try:
        updated_project = await update_project(project_id=project_id, project=project)
        return {
            "message": "project is updated",
            "data": updated_project
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{project_id}")
async def delete_project_and_role(
    project_id: UUID,
    token_data: dict = Depends(get_payload)
):
    # Dynamically generate the role name based on the project_id
    role_name = await get_project_role_name(project_id=project_id)
    user_id = token_data["sub"]

    # Check if the user has the role
    if not await has_role_bool(role_name)(token_data):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have the required role to update this project"
        )
    
    try:
        deleted_project = await delete_project(project_id=project_id)
        await revoke_role(user_id=user_id, role_name=role_name)
        await delete_role(role_name=role_name)
        return {
            "message": "project is updated",
            "data": deleted_project
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )