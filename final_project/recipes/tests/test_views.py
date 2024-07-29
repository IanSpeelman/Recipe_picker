from django.test import  TestCase
from django.urls import reverse
import unittest

class test_index(TestCase):
    
    def test_index_GET(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

class test_login(TestCase):

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Not implemented yet")
    def test_login_POST_correct_credentials(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 302)
        

    @unittest.skip("Not implemented yet")
    def test_login_POST_incorrect_credentials(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 401)
        pass

    @unittest.skip("Not implemented yet")
    def test_login_POST_incomplete_credentials(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 406)
        pass


class test_register(TestCase):

    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_POST_allowed_information(self):
        response = self.client.post(reverse("register"), {
            "username": "spielmeister",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        self.assertEqual(response.status_code, 302)
        pass

    def test_register_POST_missing_information(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        self.assertEqual(response.status_code, 406)
        pass

    def test_register_POST_passwords_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "spielmeister",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "passwordd",
            "password-confirmation": "password",
        })
        self.assertEqual(response.status_code, 406)
        pass

    def test_register_POST_emails_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "spielmeister",
            "email": "spielmeister@gmial.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        self.assertEqual(response.status_code, 406)
        pass

    def test_register_POST_duplicate_user(self):
        response = self.client.post(reverse("register"), {
            "username": "spielmeister",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        response = self.client.post(reverse("register"), {
            "username": "spielmeister",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        self.assertEqual(response.status_code, 409)
        pass