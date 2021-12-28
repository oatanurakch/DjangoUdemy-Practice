from django.db.models import query
from watchlist_app.models import *
from watchlist_app.api.serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
# ScopedRateThrottle สามารถสร้าง throttle Scope ภายในไฟล์นี้ได้เลยโดยไม่ต้องสร้าง class * CTRL + F ScopedRateThrottle * ตั้งจำนวนการ request ได้ที่หน้า setting.py
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from watchlist_app.api.permission import IsAdminorReadOnly, IsReviewUserorReadOnly
from watchlist_app.api.throtting import *
# from watchmate.watchlist_app.api.permission import IsAdminorReadOnly

#################### Class-based views ####################

class UserReview(generics.ListAPIView):
    # throttle_classes = [ReviewListThrotting, AnonRateThrottle]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     # review_user เป็น ForeignKey ถ้าต้องการเข้าถึงข้อมูลของตัวที่เป็นตัวถูกอ้างถึงให้ใช้ __ [Underscore 2 ตัว] ต่อด้วย columnname ที่ต้องการเข้าถึง เช่น username
    #     return Review.objects.filter(review_user__username = username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username = username)
    
class ReviewCreate(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    # ใช้สำหรับจำกัดจำนวนการ Request
    throttle_classes = [ReviewCreateThrotting]
    serializer_class = ReviewSerializer
    
    ''' perform_create ใช้สำหรับการ create ข้อมูล [ POST ] Request 
    นอกจากนี้ยังสามารถใช้การ put หรือ delete ได้อีกต้วย
    https://www.django-rest-framework.org/api-guide/generic-views/#createapiview '''
    
    def perform_create(self,serializer):
        
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk = pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist = watchlist, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist = watchlist, review_user = review_user)
        

''' https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview '''

class ReviewList(generics.ListCreateAPIView):
    throttle_classes = [ReviewListThrotting, AnonRateThrottle]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserorReadOnly]
    throttle_classes = [ScopedRateThrottle]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_scope = 'review-detail'

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

''' viewsets.ModelViewSet สามารถใช้งาน HTTP METHOD ได้ทุกอย่าง [GET, POST, PATCH, PUT, DELETE] '''
''' viewsets.ReadOnlyModelViewSet สามารถใช้งานได้แค่เรียกดูทั้งหมดและเรียกดูเฉพาะตัวที่ต้องการเท่านั้น '''
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminorReadOnly]
    
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
class StreamPlatformAV(APIView):
    
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many = True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class StreamPlatformDetailAV(APIView):
    
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request, pk):
        
        try:
            platform = StreamPlatform.objects.get(pk = pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error' : 'Not found'}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)
        
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk = pk)
        serializer = StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk = pk)
        platform.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        

class WatchListAV(APIView):
    
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchListDetailAV(APIView):
    
    permission_classes = [IsAdminorReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk = pk)
            serializer = WatchListSerializer(movie)
            return Response(serializer.data)
        except WatchList.DoesNotExist:
            return Response({'error' : 'Not found'}, status = status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        # if you use PUT, You should always selected object before save data and call serializer in next line
        movie = WatchList.objects.get(pk = pk)
        # next line WatchListSerializer is 2 argument movie is old data ( instance ) , request.data is new data ( validated_data )
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk = pk)
        movie.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
#################### Class-based views ####################





#################### Function based views ####################
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many = True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         except Movie.DoesNotExist:
#             return Response({'error' : 'Movie not found'}, status = status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         # if you use PUT, You should always selected object before save data and call serializer next line
#         movie = Movie.objects.get(pk = pk)
#         # next line MovieSerializer is 2 argument movie is old data ( instance ) , request.data is new data ( validated_data )
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response(status = status.HTTP_204_NO_CONTENT)

#################### Function based views ####################