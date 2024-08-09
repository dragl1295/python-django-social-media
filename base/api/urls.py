from django.urls import include, path
from .views import UserView,UserRoomViewSet,UserRoomMessageViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'rooms',RoomView)
# router.register(r'messages',MessageView)
router.register(r'users', UserView)
router.register(r'users/(?P<user_id>\d+)/rooms', UserRoomViewSet, basename='user-rooms')
router.register(r'users/(?P<user_id>\d+)/rooms/(?P<room_id>\d+)/messages', UserRoomMessageViewSet, basename='user-room-messages')


urlpatterns = [
    # path('',  views.getRoutes),
     path('', include(router.urls)),
     path('register/', views.RegisterView.as_view()),


    # path('users/', views.getUser),
    # path('rooms/<str:pk>/', views.getRoom),
    # path('<str:pk>/create-room/', views.createRoom),
]
