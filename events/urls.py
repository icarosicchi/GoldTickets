from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),  # edite esta linha
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'), # adicione esta linha
    path('search/', views.search, name='search'), # adicione esta linha
    path('create/', views.EventCreateView.as_view(), name='create'), # adicione esta linha
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete'),
    path('<int:event_id>/comment/', views.create_comment, name='comment'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories<int:pk>', views.CategoryDetailView.as_view(), name='detail-category'),
    path('<int:event_id>/buy_ticket', views.buy_tickets, name='buy-ticket'),
    path('user_events/', views.user_events, name='user_events'),
    path('user_tickets/', views.user_tickets, name='user_tickets'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket-detail'),
]