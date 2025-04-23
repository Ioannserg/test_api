from constant import BASE_URL


class TestBookings:

    def test_create_booking(self, booking_data, auth_session):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID букинга не найден в ответе"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        booking_data_response = get_booking.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


    def test_get_all_booking(self, auth_session):
        response = auth_session.get(f"{BASE_URL}/booking")
        assert response.status_code == 200, "Ошибка при получении списка бронирований"
        bookings = response.json()
        assert isinstance(bookings, list), "Ответ не является списком"
        assert len(bookings) > 0, "Список бронирований пуст"

        # Проверка структуры каждого букинга
        for booking in bookings:
            assert "bookingid" in booking, "У букинга нет ID"
            assert isinstance(booking["bookingid"], int), "ID букинга не является числом"

    def test_get_bookings_by_name(self, auth_session, booking_data):
        # Создаём букинг для фильтрации
        create_response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_response.json()["bookingid"]

        # Пытаемся найти букинг по имени
        response = auth_session.get(f"{BASE_URL}/booking?firstname={booking_data['firstname']}")
        assert response.status_code == 200
        bookings = response.json()
        assert any(b["bookingid"] == booking_id for b in bookings), "Букинг не найден по имени"

        # Удаляем тестовый букинг
        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_full_update_booking(self, auth_session, booking_data):
        # Создаём букинг
        create_response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_response.json()["bookingid"]



        # Обновляем букинг
        update_response = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data)
        assert update_response.status_code == 200, "Ошибка при обновлении"

        # Проверяем, что данные изменились
        get_response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_response.json() == booking_data, "Данные не обновились"

        # Удаляем букинг
        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_update_nonexistent_booking(self, auth_session, booking_data):
        fake_booking_id = 999999  # Несуществующий ID
        response = auth_session.put(f"{BASE_URL}/booking/{fake_booking_id}", json=booking_data)
        assert response.status_code == 405, "Ожидалась ошибка 404"

    def test_partial_update_booking(self, auth_session, booking_data):
        create_response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_response.json()["bookingid"]

        # Обновляем только имя
        patch_data = {"firstname": "NEW_NAME"}
        patch_response = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=patch_data)
        assert patch_response.status_code == 200

        # Проверяем, что изменилось только имя
        get_response = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_response.json()["firstname"] == "NEW_NAME"
        assert get_response.json()["lastname"] == booking_data["lastname"]  # Остальные поля не изменились

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_patch_invalid_data(self, auth_session, booking_data):
        create_response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_response.json()["bookingid"]

        patch_data = {"totalprice": -1}  # Невалидное значение
        patch_response = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=patch_data)

        print(patch_response.json())
        assert patch_response.status_code == 200, "Ожидалась 200"

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_delete_already_deleted_booking(self, auth_session, booking_data):
        create_response = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_response.json()["bookingid"]

        # Удаляем букинг
        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

        # Пытаемся удалить ещё раз
        second_delete = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert second_delete.status_code == 405, "Ожидалась ошибка 404"