from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app.models import *

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username  = 'example', password = 'example123')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        
        self.stream = StreamPlatform.objects.create(name = "Netflix", about = "#1 Straming Platform", website = "https://netflix.com")
    
    def test_streamplatform_create(self):
        data = {
            "name" : "Netflix",
            "about" : "#1 Straming Platform",
            "website" : "https://netflix.com"
        }
        
        response = self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # ind ย่อมาจาก Individual
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail', args = (self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username  = 'example', password = 'example123')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name = "Netflix", about = "#1 Straming Platform", website = "https://netflix.com")
        self.watchlist = WatchList.objects.create(platform = self.stream, title = "Example Movie", storyline = 'Example Movie', active = True)
    
    def test_watchlist_create(self):
        data = {
            "title" : "Example Movie",
            "storyline" : "Example Storyline!",
            "platform" : self.stream,
            "active" : True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args = (self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # การ get เฉพาะ field ใด filed หนึ่ง เช่น title [ field ชื่ออะไรก็ดูเอาใน Model นั้น ๆ ]
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertEqual(WatchList.objects.get().title, 'Example Movie')
        
class ReviewTestCase(APITestCase):
    
    # self.parameter ที่สร้างขึ้นใน def setUp 1 ตัวเมื่อเอาไปใช้ในการ Test จะดึงข้อมูลมาใช้ใน Setup ไม่ได้
    def setUp(self):
        self.user = User.objects.create_user(username  = 'example', password = 'example123')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name = "Netflix", about = "#1 Straming Platform", website = "https://netflix.com")
        # Watclist ตัวนี้ใช้สำหรับการ Test การสร้าง Watchlist
        self.watchlist = WatchList.objects.create(platform = self.stream, title = "Example Movie", storyline = 'Example Movie', active = True)
        # สร้าง Watchlist2 ขึ้นมาอีกตัวเพื่อนำไปใช้ในการ Test Review create
        self.watchlist2 = WatchList.objects.create(platform = self.stream, title = "Example Movie", storyline = 'Example Movie', active = True)
        self.review = Review.objects.create(review_user = self.user, rating = 5, description = 'Great Movie!', watchlist = self.watchlist2, active = True)
        
    def test_review_create(self):
        data = {
            "review_user" : self.user.id,
            "rating" : 5,
            "description" : "Great movie!",
            "watchlist" : self.watchlist,
            "active" : True
        }
        response = self.client.post(reverse('reviewcreate', args = (self.watchlist.id,)), data = data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        # self.assertEqual(Review.objects.get().rating, 5)
        response = self.client.post(reverse('reviewcreate', args = (self.watchlist.id,)), data = data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # ใช้สำหรับทดสอบการ POST Data โดยไม่มีการ Authenticate โดยการใช้ force_authenticate
    def test_review_create_unauth(self):
        data = {
            "review_user" : self.user.id,
            "rating" : 5,
            "description" : "Great movie!",
            "watchlist" : self.watchlist,
            "active" : True
        }
        
        self.client.force_authenticate(user = None)
        response = self.client.post(reverse('reviewcreate', args = (self.watchlist.id,)), data = data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        
        data = {
            "review_user" : self.user.id,
            "rating" : 4,
            "description" : "Great movie! - Updated!",
            "watchlist" : self.watchlist,
            "active" : False
        }
        response = self.client.put(reverse('review-detail', args = (self.review.id,)), data = data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args = (self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_user(self):
        response = self.client.get('watch/review?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)