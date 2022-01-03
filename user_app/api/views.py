from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# ถ้าใช้ JWT Token ให้เอา models ออกเนื่องจาก models เป็นการสร้าง Token อัตโนมัติ
from user_app import models
from user_app.api.serailizers import *

@api_view(['POST',])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful !"
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.get(user = account).key
            data['token'] = token
            
            # ใช้สร้าง Token ทันทีเมื่อมีการ Register สำเร็จ
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }
        else:
            data = serializer.errors
        
        return Response(data, status = status.HTTP_201_CREATED)