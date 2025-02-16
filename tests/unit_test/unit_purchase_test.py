from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.crud.auth import add_user
from app.crud.inventory import add_purchase_to_inventory, get_all_inventory
from app.crud.product import get_product_by_name, get_product_by_id



from app.services.auth import get_password_hash

pytestmark = pytest.mark.anyio


async def test_get_product(session: AsyncSession) -> None:
    test_product = {
        'name': 'cup',
        'price': 20
    }

    product_by_name = await get_product_by_name(session, test_product['name'])
    assert product_by_name is not None
    assert product_by_name.name == test_product['name']
    assert product_by_name.price == test_product['price']

    product_by_id = await get_product_by_id(session, product_by_name.id)
    assert product_by_id is not None
    assert product_by_id.name == test_product['name']
    assert product_by_id.price == test_product['price']


async def test_add_get_inventory(session: AsyncSession):
    user_1_info = {
        "username": "user1",
        "password": "user1_password",
        "hashed_password": get_password_hash("user1_password"),
    }
    user_1 = await add_user(user_1_info['username'], user_1_info['hashed_password'], session)

    test_product = {
        'name': 'cup',
        'price': 20
    }
    product_by_name = await get_product_by_name(session, test_product['name'])

    inventory = await add_purchase_to_inventory(session, product_by_name.id, user_1.id)
    assert inventory is not None
    assert inventory.quantity == 1

    inventory_2 = await add_purchase_to_inventory(session, product_by_name.id, user_1.id)
    assert inventory_2 is not None
    assert inventory.quantity == 2

    all_inventory = await get_all_inventory(session, user_1.id)
    assert len(all_inventory) == 1
    assert all_inventory[0].type == product_by_name.name
    assert all_inventory[0].quantity == 2









