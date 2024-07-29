from django.test import  TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import unittest

class test_index(TestCase):
    
    def test_index_GET(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

class test_login(TestCase):
    def setUp(self):
        User.objects.create_user(username="test_user", password="password")

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_POST_correct_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"test_user",
            "password": "password"
        })
        self.assertEqual(response.status_code, 302)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "test_user")

    def test_login_POST_incorrect_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"spielmiester",
            "password": "password"
        })
        self.assertEqual(response.status_code, 401)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")

    def test_login_POST_incomplete_credentials(self):
        response = self.client.post(reverse("login"),{
            "username":"test_user",
            "password": ""
        })
        self.assertEqual(response.status_code, 406)
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")


class test_register(TestCase):

    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_POST_allowed_information(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "test_user")
        self.assertEqual(response.status_code, 302)

    def test_register_POST_missing_information(self):
        response = self.client.post(reverse("register"), {
            "username": "",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    def test_register_POST_passwords_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmail.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "passwordd",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    def test_register_POST_emails_no_match(self):
        response = self.client.post(reverse("register"), {
            "username": "test_user",
            "email": "spielmeister@gmial.com",
            "email-confirmation": "spielmeister@gmail.com",
            "password": "password",
            "password-confirmation": "password",
        })
        request = response.wsgi_request
        self.assertEqual(request.user.username, "")
        self.assertEqual(response.status_code, 406)

    # def test_register_POST_duplicate_user(self):
    #     response = self.client.post(reverse("register"), {
    #         "username": "test_user",
    #         "email": "spielmeister@gmail.com",
    #         "email-confirmation": "spielmeister@gmail.com",
    #         "password": "password",
    #         "password-confirmation": "password",
    #     })
    #     response = self.client.post(reverse("register"), {
    #         "username": "test_user",
    #         "email": "spielmeister@gmail.com",
    #         "email-confirmation": "spielmeister@gmail.com",
    #         "password": "password",
    #         "password-confirmation": "password",
    #     })
    #     self.assertEqual(response.status_code, 409)