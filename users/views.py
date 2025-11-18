from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, ParentProfileSerializer, ChildProfileSerializer
from .models import ParentProfile, ChildProfile


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class TokenObtainView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # simple credential login endpoint (username or email + password)
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token), 'refresh': str(refresh)})
        return Response({'detail': 'username and password required'}, status=status.HTTP_400_BAD_REQUEST)


class ParentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ParentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = ParentProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChildListCreateView(generics.ListCreateAPIView):
    serializer_class = ChildProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile, _ = ParentProfile.objects.get_or_create(user=self.request.user)
        return ChildProfile.objects.filter(parent=profile)

    def perform_create(self, serializer):
        profile, _ = ParentProfile.objects.get_or_create(user=self.request.user)
        serializer.save(parent=profile)


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChildProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        profile, _ = ParentProfile.objects.get_or_create(user=self.request.user)
        return ChildProfile.objects.filter(parent=profile)
