from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, TokenObtainView, ParentProfileView, ChildListCreateView, ChildDetailView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/parent/', ParentProfileView.as_view(), name='parent_profile'),
    path('children/', ChildListCreateView.as_view(), name='children-list'),
    path('children/<int:pk>/', ChildDetailView.as_view(), name='children-detail'),
]
