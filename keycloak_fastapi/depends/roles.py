from keycloak import KeycloakAdmin
from core.settings import settings, settings_env
from typing import Optional
from api.schemas import RoleRepresentation
from fastapi import HTTPException
from fastapi import status

keycloak_admin = KeycloakAdmin(server_url=settings.server_url,
                               realm_name=settings.realm,
                               client_id=settings.client_id,
                               client_secret_key=settings.client_secret,
                               verify=True)

async def create_role(role_name: str, description: Optional[str]):
    try:
        client_uuid = await keycloak_admin.a_get_client_id(client_id=settings.client_id)
        payload = {
            "name": role_name,
            "description": description
        }
        return await keycloak_admin.a_create_client_role(client_role_id=client_uuid, payload=payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def delete_role(role_name: str):
    try:
        client_uuid = await keycloak_admin.a_get_client_id(client_id=settings.client_id)
        await keycloak_admin.a_delete_client_role(client_role_id=client_uuid, role_name=role_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def assign_role(user_id: str, role_name: str):
    try:
        client_uuid = await keycloak_admin.a_get_client_id(client_id=settings.client_id)
        role_id = await keycloak_admin.a_get_client_role_id(client_id=client_uuid, role_name=role_name)
        role = RoleRepresentation(
            id=role_id,
            name=role_name
        ) 
        await keycloak_admin.a_assign_client_role(client_id=client_uuid, user_id=user_id, roles=[role.model_dump()])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

async def revoke_role(user_id: str, role_name: str):
    try:
        client_uuid = await keycloak_admin.a_get_client_id(client_id=settings.client_id)
        role_id = await keycloak_admin.a_get_client_role_id(client_id=client_uuid, role_name=role_name)
        role = RoleRepresentation(
            id=role_id,
            name=role_name
        ) 
        await keycloak_admin.a_delete_client_roles_of_user(user_id=user_id, client_id=client_uuid, roles=[role.model_dump()])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)  
        )
