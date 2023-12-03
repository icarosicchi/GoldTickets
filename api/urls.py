from django.urls import path
from .views import EventList, EventDetail, CommentList, CommentDetail

urlpatterns = [
    path('events/<int:pk>/', EventDetail.as_view()),
    path('events/', EventList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('comments/', CommentList.as_view()),
]