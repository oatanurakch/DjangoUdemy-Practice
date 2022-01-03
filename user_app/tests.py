# https://www.django-rest-framework.org/api-guide/testing/#testing


# reverse ใช้สำหรับเรียก url ผ่าน name ที่ตั้งไว้ในการประกาศ path ซึ่งโดยปกติเราจะเรียก URL ผ่าน URL ที่ตั้งไว้แต่ถ้าใช้ reverse จะสามารถเรียกผ่านชื่อที่ประกาศไว้ได้เลย
from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username" : "testcase",
            "email" : "testcase@example.com",
            "password" : "testcase",
            "password2": "testcase"
        }    
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogoutTestCase(APITestCase):
    
    # setUp ใช้สำหรับทดสอบการสร้าง Username ขึ้นมาก่อนเพื่อใช้ในการ test login
    def setUp(self):
        self.user = User.objects.create_user(username = "example10", password = "example10")
        
    def test_logint(self):
        data = {
            "username" : "example10",
            "password" : "example10"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # การ logout นั้นจำเป็นต้องส่ง Token ของ User นั้น ๆ ที่ได้จากการ login หรือ register ส่งไปใน header
    # https://www.django-rest-framework.org/api-guide/testing/#authenticating
    def test_logout(self):
        
        self.token = Token.objects.get(user__username = "example10")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        