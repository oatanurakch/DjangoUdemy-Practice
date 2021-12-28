from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrotting(UserRateThrottle):
    scope = 'review-create'
    
class ReviewListThrotting(UserRateThrottle):
    scope = 'review-list'