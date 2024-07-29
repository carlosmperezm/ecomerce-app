from django.urls import URLPattern,URLResolver,path

from users.views import UserListView,UserDetailView,SignupView,LoginView

urlpatterns:list[URLPattern|URLResolver]=[
        path('',UserListView.as_view(),name='user-list'),
        path('<int:pk>/',UserDetailView.as_view(),name='user-detail'),
        path('signup/',SignupView.as_view(),name='signup'),
        path('login/',LoginView.as_view(),name='login'),
        ]
