from django.test import TestCase
from rest_framework.test import APITestCase
from . import models
from users.models import User

# Create your tests here.


class TestAmenities(APITestCase):

    NAME = "amenity test"
    DESC = "description of amenitiy test"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self) -> None:
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get("/api/v1/rooms/amenities/")
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "statuscode is not 200",
        )

        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):

        new_amenity_name = "New Amenity Name"
        new_amenity_description = "New Description"
        response = self.client.post(
            self.URL,
            data={"name": new_amenity_name, "descpiption": new_amenity_description},
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "statuscode is not 200",
        )
        data["name"]
        response = self.client.post(self.URL, data)
        data = response.json()
        self.assertNotEqual(
            response.status_code,
            400,
            "bad reqeust",
        )


class TestAmenity(APITestCase):

    NAME = "Test amenity"
    DESC = "Test Amenity Descriptiion"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404, "404 BAD reqeust!")

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["name"], self.NAME)

    def test_put_amenity(self):
        response = self.client.put(
            "/api/v1/rooms/amenities/1",
            {"name": self.NAME, "description": self.DESC},
        )

        print("stats:", response.status_code)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1")
        self.assertEqual(response.status_code, 204)


class Test_Rooms(APITestCase):
    def setUp(self):

        user = User.objects.create(
            username="test",
        )

        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.post("/api/v1/rooms/")

        print(response.json())
