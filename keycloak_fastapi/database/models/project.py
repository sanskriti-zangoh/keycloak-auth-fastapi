from database.models.base import VSQLModel, VSQLModelType
from sqlmodel import Field, Column, select, Relationship
from datetime import datetime
from typing import Optional, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String

ProjectType = TypeVar("ProjectType", bound="Project")



class Project(VSQLModel, table=True):

    """
    Users model for the registered users.

    Fields:
        id: ID of the user.
        name: Name of the user.
        username: Username of the user.
        email: Email of the user.
        active: If True, the user is active.
        created_at: Created at.
        updated_at: Last Updated at.
    """
    name: str = Field(index=True, nullable=False, unique=True)
    description: Optional[str] = Field(sa_column=Column(String, nullable=True))

    @classmethod
    async def get_by_name(cls: Type[ProjectType], name: str, session: AsyncSession) -> ProjectType:
        """
        Get a user by username.

        Args:
            username (str): Username of the user.
            session (AsyncSession): An async session.

        Returns:
            UsersType: A user.
        """
        data = await session.execute(select(cls).where(cls.name == name))
        data = data.scalar_one_or_none()
        return data
    