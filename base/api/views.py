from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room,User,Message
from .serializers import RoomSerializer, UserSerializer,MessageSerializer,RegisterSerializer
from rest_framework import status, viewsets,generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission




class IsHostOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.POST.get() == request.user
       
    
class IsMessageHostOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return self.kwargs.get('user_id') == request.user



class UserRoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated,IsHostOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        return Room.objects.filter(host=user)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        serializer.save(host=self.request.user)
    
class UserRoomMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageHostOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        room_id = self.kwargs.get('room_id')
        try:
            user = User.objects.get(pk=user_id)
            room = Room.objects.get(pk=room_id, host=user)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        except Room.DoesNotExist:
            raise NotFound("Room not found.")
        return Message.objects.filter(room=room)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        room_id = self.kwargs.get('room_id')
        print(f"Creating message for user {user_id} in room {room_id}")  # Debug output

        try:
            user = User.objects.get(pk=user_id)
            room = Room.objects.get(pk=room_id, host=user)
        except User.DoesNotExist:
            raise NotFound("User not found.")
        except Room.DoesNotExist:
            raise NotFound("Room not found.")
        serializer.save(user=self.request.user, room=room)   
    
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token for the new user
        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)    
    
    
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   
    permission_classes = [IsAuthenticated, IsHostOrReadOnly]
    def get_queryset(self):
        # Optionally filter users based on the request
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         'GET /api',
#         'GET /api/rooms',
#         'GET /api/rooms/:id'
#     ]
#     return Response(routes)


# @api_view(['GET'])
# def getRooms(request):
#     rooms = Room.objects.all()
#     serializer = RoomSerializer(rooms, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def getRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     serializer = RoomSerializer(room, many=False)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getUser(request):
#     user = User.objects.all()
#     serializer = UserSerializer(user, many=True)

#     return Response(serializer.data)
#     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def createRoom(request, pk):
#     user = User.objects.get(pk=pk)
#     data = request.data
#     data['host'] = user.id  # Add the host to the data

#     serializer = RoomSerializer(data=data)
#     print(serializer)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
