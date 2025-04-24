import pytest
from constant import BASE_URL


class TestItems:
    endpoint = f"{BASE_URL}/items/"

    def test_create_item(self, item_data, auth_session):

        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        data = response.json()
        item_id = data.get("id")
        owner_id = data.get("owner")
        assert item_id is not None, 'id не найден'
        assert data.get("title") == item_data["title"]
        assert data.get("description") == item_data["description"]

        self.created_item_id = item_id
        self.owner_id = owner_id

        response_get_items_id = auth_session.get(f'{self.endpoint}{self.created_item_id}')
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"
        assert response_get_items_id.json().get("title") == item_data["title"]
        assert response_get_items_id.json().get("description") == item_data["description"]
        assert response_get_items_id.json().get("id") == self.created_item_id
        assert response_get_items_id.json().get("owner") == self.owner_id



    def test_create_borderline(self, auth_session):
        data = {
            "title":f"012345678901234567890123456789012345678901234567890123456789"
                    f"012345678901234567890123456789012345678901234567890123456789"
                    f"012345678901234567890123456789012345678901234567890123456789"
                    f"012345678901234567890123456789012345678901234567890123456789012345678901234",
            "description":""
        }
        response = auth_session.post(self.endpoint, json=data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        data = response.json()
        item_id = data.get("id")
        owner_id = data.get("owner")
        assert item_id is not None, 'id не найден'
        assert data.get("title") == data["title"]
        assert data.get("description") == data["description"]

        self.created_item_id = item_id
        self.owner_id = owner_id

        response_get_items_id = auth_session.get(f'{self.endpoint}{self.created_item_id}')
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"
        assert response_get_items_id.json().get("title") == data["title"]
        assert response_get_items_id.json().get("description") == data["description"]
        assert response_get_items_id.json().get("id") == self.created_item_id
        assert response_get_items_id.json().get("owner") == self.owner_id


    def test_get_items(self, auth_session):
        response = auth_session.get(self.endpoint)
        assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"

        data = response.json()
        assert "data" in data, "Response missing 'data' key"
        assert isinstance(data["data"], list), "'data' is not a list"
        assert isinstance(data.get("count"), int), "'count' should be integer"



    def test_get_pagination(self, auth_session):
        for i in range(7):
            page = f'?page={i}'

            response = auth_session.get(f'{self.endpoint}{page}')
            assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"
            data = response.json()
            assert "data" in data, "Response missing 'data' key"
            assert isinstance(data["data"], list), "'data' is not a list"
            assert isinstance(data.get("count"), int), "'count' should be integer"

    # def test_get_filter(self, auth_session):
    #     response = auth_session.get(f'{self.endpoint}?title=Reach')
    #     assert response.status_code == 200, f"Response: {response.status_code}, {response.text}"
    #     data = response.json()
    #     assert "data" in data, "Response missing 'data' key"
    #     assert data.get("count") == 20, 'Их почему то не 20'



    def test_put_items(self, auth_session, item_data):
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        item_id = response.json().get("id")
        self.item_id = item_id

        put_items = auth_session.put(f'{self.endpoint}{self.item_id}', json={"title":"TEST123456", "description":"TEST_description"})


        assert put_items.status_code == 200, f"Response: {put_items.status_code}, {put_items.text}"
        assert put_items.json().get("title") == "TEST123456"
        assert put_items.json().get("description") == "TEST_description"



    def test_delete_item(self, auth_session, item_data):
        response = auth_session.post(self.endpoint, json=item_data)
        assert response.status_code in (200, 201), f"Response: {response.status_code}, {response.text}"

        item_id = response.json().get("id")
        self.item_id = item_id

        delete_item = auth_session.delete(f'{self.endpoint}{self.item_id}')
        assert delete_item.status_code == 200, f"Response: {delete_item.status_code}, {delete_item.text}"

        get_deleted_item = auth_session.get(f'{self.endpoint}{self.item_id}')
        assert get_deleted_item.status_code in (422, 404)

        delete_item_again = auth_session.delete(f'{self.endpoint}{self.item_id}')
        assert delete_item_again.status_code in (422, 404)




