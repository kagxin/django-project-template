from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from apps.utils.jwt.views import obtain_jwt_check_token_change, refresh_jwt_check_token_change,\
    verify_jwt_check_token_change

urlpatterns = [
    path('token/', obtain_jwt_check_token_change),
    path('token/refresh/', refresh_jwt_check_token_change),
    path('token/verify/', verify_jwt_check_token_change),

    # for SessionAuthentication
    path('auth/', include('rest_framework.urls')),
]
