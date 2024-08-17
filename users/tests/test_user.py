"""Test for the user Model"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.tests.base import BaseTest
from users.models import User

PERMISSION_ERROR: str = "You do not have permission to perform this action."


class SignUpTest(BaseTest):
    """Test class if the user can sign up"""

    def test_signup(self) -> None:
        """sign up the user"""
        response: Response = self.client.post(self.signup_url, self.user_data)
        # quantity: int = 5
        # self.create_address(quantity)
        # self.client.put(reverse("user-detail", args=[1]), {"address": 1})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("username"),
            self.user_data.get("username"),
        )
        self.assertEqual(response.data.get("email"), self.user_data.get("email"))
        self.assertEqual(
            response.data.get("phone_number"), self.user_data.get("phone_number")
        )

    def test_signup_invalid_data(self) -> None:
        """test if the user insert not data the api responds with a 400 error code"""
        response: Response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(BaseTest):
    """class for login tests"""

    def test_login(self) -> None:
        """test if the user has logged correctly"""

        payload: dict[str, str] = {
            "username": "testuser1",
            "password": "testpassword",
            "email": "1test@test.com",
        }
        self.create_users(1)

        response: Response = self.client.post(
            self.login_url,
            payload,
        )

        user: User = User.objects.get(pk=1)
        token: Token = Token.objects.get(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("token"), token.key)
        self.assertIsNotNone(response.data)

    def test_login_invalid_data(self) -> None:
        """Check if the user no insert any data to log in.
        The porgram should respond with a 400 error code"""
        self.create_users(2)
        # self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error"), "Username, password and email are required"
        )

    def test_login_invalid_user(self) -> None:
        """test if the user insert no valid password or no valid username
        The program should return 400 bad request"""
        self.create_users(1)
        # self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(
            self.login_url,
            {
                "username": "invaliduser",
                "password": "invalidpassword",
                "email": "invalidemail",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("error"), "Invalid credentials")


class UserGetTest(BaseTest):
    """Test for the user detail view"""

    def test_get_all_users_as_admin(self) -> None:
        """Test if the user can access the user list view as an admin"""

        user_quantity: int = 5
        self.create_users(user_quantity)
        self.create_user_admin(
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword",
            }
        )
        self.client.login(username="admin", password="adminpassword")

        response: Response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), user_quantity + 1)

    def test_get_all_users_as_no_admin(self) -> None:
        """Test if the user can access the user list view as a regular user"""
        self.create_users(3)
        self.client.login(username="testuser1", password="testpassword")
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(
            response.data.get("detail"),
            PERMISSION_ERROR,
        )

    def test_get_all_users_with_invalid_auth(self) -> None:
        """Theest if the user can access the user list view with an invalid token"""
        self.create_users(quantity=3)
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Invalid token.",
        )

        self.client.credentials()
        self.client.login(username="invalidusername", password="testpassword")
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_get_all_users_without_login(self) -> None:
        """Test if the user can access the user list view without login"""
        self.create_users(5)
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_as_regular_user_with_no_permission(self) -> None:
        """Test if the user cannot be accessed by a regular user if it is not the same user"""
        self.create_users(4)

        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.get(self.user_detail_url(2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            PERMISSION_ERROR,
        )

        response = self.client.get(self.user_detail_url(3))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            PERMISSION_ERROR,
        )

    def test_get_user_as_regular_user_with_permission(self) -> None:
        """Test if the user can be accessed by a regular user if it is the same user"""
        self.create_users(2)

        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.get(self.user_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("username"), "testuser1")
        self.assertEqual(response.data.get("email"), "1test@test.com")

    def test_get_user_as_admin(self) -> None:
        """Test if any user can be accessed by an admin"""
        self.create_users(3)
        self.create_user_admin(
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword",
            }
        )
        self.client.login(username="admin", password="adminpassword")

        response: Response = self.client.get(self.user_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("username"), "testuser1")
        self.assertEqual(response.data.get("email"), "1test@test.com")

        response = self.client.get(self.user_detail_url(3))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("username"), "testuser3")
        self.assertEqual(response.data.get("email"), "3test@test.com")


class UserDeleteTest(BaseTest):
    """Test for the user delete view"""

    def test_delete_user_as_admin(self) -> None:
        """Test if the user can be deleted by an admin"""
        self.create_users(3)  # 3 regular users
        self.create_user_admin(
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword",
            }
        )  # 1 admin user , 4 total users

        self.client.login(username="admin", password="adminpassword")

        response: Response = self.client.delete(self.user_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            User.objects.count(), 3
        )  # 4 users(1 admin,3 regular users) - 1 deleted = 3

        response = self.client.delete(self.user_detail_url(2))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            User.objects.count(), 2
        )  # 3 users(1 admin,2 regular users) - 1 deleted = 2

    def test_delete_user_as_regular_user_with_no_permission(self) -> None:
        """Test if the user cannot be deleted by a regular user if it is not the same user"""
        self.create_users(3)
        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.delete(self.user_detail_url(2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            PERMISSION_ERROR,
        )
        self.assertEqual(User.objects.count(), 3)

    def test_delete_user_as_regular_user_with_permission(self) -> None:
        """Test if the user can be deleted by a regular user if it is the same user"""
        self.create_users(2)
        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.delete(self.user_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_delete_user_with_invalid_auth(self) -> None:
        """Test if the user can be deleted with an invalid token"""
        self.create_users(3)

        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        response: Response = self.client.delete(self.user_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Invalid token.",
        )

        self.client.credentials()
        response = self.client.delete(self.user_detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )


class UserUpdateTest(BaseTest):
    """Test for the user update view"""

    data_to_update: dict[str, str] = {
        "username": "testuser1updated",
        "email": "updatedemail@test.com",
        "phone_number": "123456789",
        "password": "updatedpassword",
    }

    def test_update_user_as_admin(self) -> None:
        """Test if the user can be updated by an admin"""
        self.create_users(3)
        self.create_user_admin(
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword",
            }
        )

        self.client.login(username="admin", password="adminpassword")
        response: Response = self.client.put(
            self.user_detail_url(2), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, response.data.pop("id"))
        self.assertEqual(
            self.data_to_update.get("username"), response.data.get("username")
        )
        self.assertEqual(self.data_to_update.get("email"), response.data.get("email"))
        self.assertEqual(
            self.data_to_update.get("phone_number"), response.data.get("phone_number")
        )

    def test_update_user_as_regular_user_with_no_permission(self) -> None:
        """Test if the user cannot be updated by a regular user if it is not the same user"""
        self.create_users(3)
        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.put(
            self.user_detail_url(2), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            PERMISSION_ERROR,
        )

    def test_update_user_as_regular_user_with_permission(self) -> None:
        """Test if the user can be updated by a regular user if it is the same user"""
        self.create_users(2)
        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.put(
            self.user_detail_url(1), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.data_to_update.get("username"), response.data.get("username")
        )
        self.assertEqual(self.data_to_update.get("email"), response.data.get("email"))
        self.assertEqual(
            self.data_to_update.get("phone_number"), response.data.get("phone_number")
        )

    def test_update_user_with_invalid_auth(self) -> None:
        """Test if the user can be updated with an invalid token"""
        self.create_users(3)

        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        response: Response = self.client.put(
            self.user_detail_url(1), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"),
            "Invalid token.",
        )

        self.client.credentials()
        response = self.client.put(self.user_detail_url(1), self.data_to_update)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_update_user_with_invalid_data(self) -> None:
        """Test if the user can be updated with invalid data"""
        self.create_users(3)
        self.client.login(username="testuser1", password="testpassword")

        response: Response = self.client.put(self.user_detail_url(1), {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
