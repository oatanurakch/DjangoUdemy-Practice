from django.urls import path, include
from watchlist_app.api.views import *
from rest_framework.routers import DefaultRouter


#################### Class-based views ####################

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename = 'steamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'movie-list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = 'movie-detail'),
    path('list2/', WatchList.as_view(), name = 'movie-list'),
    path('', include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name = 'streamplatform'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name = 'streamplatform-detail'),
    
    # path('review/', ReviewList.as_view(), name = 'review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail'),
    
    path('<int:pk>/review-create', ReviewCreate.as_view(), name = 'review-create'),
    path('<int:pk>/reviews', ReviewList.as_view(), name = 'review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail'),
    
    # ตัวนี้เป็นการใช้กับ get_queryset Filtering against the URL
    # path('review/<str:username>', UserReview.as_view(), name = 'user-review-detail'),
    
    # ตัวนี้ใช้ร่วมกับ self.request.query_params.get(parameter) Filtering against query parameters
    path('review/', UserReview.as_view(), name = 'user-review-detail'),
    
]

#################### Class-based views ####################

#################### Function based views ####################

# urlpatterns = [
#     path('list/', movie_list, name = 'movie-list'),
#     path('<int:pk>', movie_detail, name = 'movie-detail')
# ]

#################### Function based views ####################