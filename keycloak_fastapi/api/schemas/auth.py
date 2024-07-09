"""
Schemas for authentication
"""

from pydantic import BaseModel, EmailStr
from uuid import UUID

class User(BaseModel):
    """
    The User model
    Fields:
        id: UUID
        username: str
        email: str
        first_name: str
        last_name: str
        realm_roles: list
        client_roles: list
    """
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    email_verified: bool
    realm_roles: list
    client_roles: list

class authConfiguration(BaseModel):
        """
        The authConfiguration model
        Fields:
            server_url: str
            realm: str
            client_id: str
            client_secret: str
            authorization_url: str
            token_url: str
        """
        server_url: str
        realm: str
        client_id: str
        client_secret: str
        authorization_url: str
        token_url: str