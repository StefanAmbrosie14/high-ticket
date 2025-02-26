from django.urls import path, include
from .views import event_list, event_detail, order_list, order_detail

urlpatterns = [
    path('api/events/', event_list, name='event-list'),
    path('api/events/<int:pk>/', event_detail, name='event-detail'),
    path('api/orders/', order_list, name='order-list'),
    path('api/orders/<int:pk>/', order_detail, name='order-detail'),
]
