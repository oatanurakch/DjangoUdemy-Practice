from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from user_app.api.views import *

# JWT Token
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#installation
# ใชแกะข้อมูล https://jwt.io/

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('login/', obtain_auth_token, name = 'login'),
    path('register/', registration_view, name = 'register'),
    path('logout/', logout, name = 'logout'),
    
    # ใช้ร่วมกับ JWT Token ในการสร้าง Token เพื่อ Access
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]