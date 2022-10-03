from django.urls import path

from user_app.apis import UserAccountCreationAPI, UserLoginAPI, UserAccountAPI, AdminUserBasicAPI

URL_PREFIX = 'api/user/'

urlpatterns = [
    path('register/', UserAccountCreationAPI.as_view(), name='user-registration'),
    path('login/', UserLoginAPI.as_view(), name='user-login'),
    path('account/', UserAccountAPI.as_view(), name='user-account'),
    path('account/admin-view/', AdminUserBasicAPI.as_view(), name='admin-user-accounts')
]