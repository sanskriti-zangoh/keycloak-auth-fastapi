from depends.roles import create_role, delete_role, assign_role, revoke_role

test_user_id = "b8d42627-993b-4441-9b75-8f5e88841834"


async def test_create_role():
    await create_role(role_name="test_role", description="test role description")


async def test_delete_role():
    await delete_role(role_name="test_role")


async def test_assign_role():
    await assign_role(user_id=test_user_id, role_name="test_role")


async def test_revoke_role():
    await revoke_role(user_id=test_user_id, role_name="test_role")

if __name__=="__main__":
    import asyncio
    asyncio.run(test_create_role())
    asyncio.run(test_assign_role())
    asyncio.run(test_revoke_role())
    asyncio.run(test_delete_role())