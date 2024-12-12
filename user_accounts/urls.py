from django.urls import path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login',views.login_user, name='login_user'),
    path('logout',views.logout_user, name='logout_user'),
    path('register',views.register_user, name='register_user'),
    path('welcome',views.welcome, name='welcome'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('edit_userprofile', views.edit_userprofile, name='edit_userprofile'),
    path('edit_userprofile_image', views.edit_userprofile_image, name='edit_userprofile_image'),
    path('edit_userprofile_details', views.edit_userprofile_details, name='edit_userprofile_details'),
    path('change_password', views.change_password, name='change_password'),
]
urlpatterns += staticfiles_urlpatterns()
 