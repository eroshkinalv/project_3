from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserUpdateView, UserDetailView, PasswordTemplateView, \
    UserListView, ManagerUpdateView, ManagerDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('create_user/', UserCreateView.as_view(), name='users_create'),
    path('list_users/', UserListView.as_view(), name='users_list'),
    path('update_user/<int:pk>/update/', UserUpdateView.as_view(), name='users_update'),
    path('detail_user/<int:pk>/detail/', UserDetailView.as_view(), name='users_detail'),
    path('email_confirm/<str:token>/', email_verification, name='email_confirm'),
    path('change_password/', PasswordTemplateView.as_view(), name='password_change'),

    path('manager_update/<int:pk>/update/', ManagerUpdateView.as_view(), name='manager_update'),
    path('manager_detail/<int:pk>/detail/', ManagerDetailView.as_view(), name='manager_detail'),
]
