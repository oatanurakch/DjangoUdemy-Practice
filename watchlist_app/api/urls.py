from django.urls import path, include
from watchlist_app.api.views import *
from rest_framework.routers import DefaultRouter


#################### Class-based views ####################

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename = 'steamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name = 'movie-list'),
    path('<int:pk>', WatchListDetailAV.as_view(), name = 'movie-detail'),
    path('', include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(), name = 'streamplatform'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name = 'streamplatform-detail'),
    
    # path('review/', ReviewList.as_view(), name = 'review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail'),
    
    path('<int:pk>/review-create', ReviewCreate.as_view(), name = 'review-create'),
    path('<int:pk>/reviews', ReviewList.as_view(), name = 'review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail'),
    
]

#################### Class-based views ####################

#################### Function based views ####################

# urlpatterns = [
#     path('list/', movie_list, name = 'movie-list'),
#     path('<int:pk>', movie_detail, name = 'movie-detail')
# ]

#################### Function based views ####################