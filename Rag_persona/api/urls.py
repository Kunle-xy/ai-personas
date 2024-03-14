from django.urls import path
from .views import documentlist, createuser, MyTokenObtainPairView, prompt
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)




urlpatterns = [
    path('', documentlist, name='document-list'),
    path('createuser/', createuser, name='create-user'),
    path('query/', prompt, name='query'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
