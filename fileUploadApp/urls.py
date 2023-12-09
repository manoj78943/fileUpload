
from django.urls import path
from . import views

urlpatterns = [
    path('', views.url_check, name='url_check'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('upload/', views.upload_file, name='file_upload'),
    path('list/', views.file_list, name='file_list'),
    path('search/', views.search_users, name='search_users'),
    path('search/results/', views.search_results, name='search_results'),
    path('share/', views.share_files, name='share_files'),
    path('developer/', views.developer, name='developer'),
    path('share-files/', views.share_files_api, name='share_files_api'),
]
